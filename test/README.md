# RAG rendszer kiértékelési útmutató (RAGAS)

Ez a dokumentáció a rendszer kiértékelési folyamatait, a használt metrikákat, a tesztfájlok pontos működési logikáját, valamint az API túlterhelésből és a **503-as hibákból** adódó problémák kiküszöbölési stratégiáit foglalja össze.

---

## 📊 Kiértékelési módszer: A RAGAS Metrikák

A rendszer teljesítményének objektív mérése a **RAGAS** keretrendszer segítségével történik. A folyamat során az alábbi 5 alapvető metrika szerint értékeljük a válaszokat és a kontextusokat. Minden metrika értéke **0.0 és 1.0 között** mozog, az eredményeket **4 tizedesjegy pontossággal** kerekítve jelenítjük meg.

### 1. Hűség (Faithfulness)
* **Mit tesztel:** Azt méri, hogy a generált válasz mennyire konzisztens a visszakeresett szöveges kontextussal.
* **Hogyan:** Kiszűri a hallucinációkat, azaz a kontextusban nem szereplő, kitalált információkat.

### 2. Válasz Relevancia (Answer Relevancy)
* **Mit tesztel:** Azt méri, hogy a generált válasz mennyire áll közvetlen összhangban a felhasználó eredeti kérdésével.
* **Hogyan:** Ellenőrzi, hogy a rendszer valóban a feltett kérdésre válaszol-e, vagy elbeszél mellette.

### 3. Kontextus Visszahívás (Context Recall)
* **Mit tesztel:** Azt méri, hogy a referenciaértékben (Ground Truth) található fontos információk közül mennyit sikerült sikeresen lekérni az adatbázisból.
* **Hogyan:** Arra összpontosít, hogy ne maradjanak ki kritikus adatok a visszakeresési fázisban.

### 4. Kontextus Precizitás (Context Precision)
* **Mit tesztel:** Azt értékeli, hogy a visszakereső (Retriever) mennyire hatékonyan rangsorolja a releváns információkat.
* **Hogyan:** Ellenőrzi, hogy a legfontosabb szövegrészek a találati lista elejére kerülnek-e, minimalizálva a zajt.

### 5. Válasz Helyessége (Answer Correctness)
* **Mit tesztel:** A generált válasz és a referenciaérték (Ground Truth) közötti szemantikai és ténybeli egyezést méri.
* **Hogyan:** A teljes folyamat végpontok közötti (end-to-end) abszolút pontosságát számszerűsíti.

---

### 🧮 A komponensek értékelésének összegzése

A metrikák alapján pontosan azonosítható, hogy a rendszer melyik fázisán szükséges finomhangolás:
* **Context Precision és Context Recall:** A **visszakereső komponenst** minősíti (megfelelőek-e a dokumentum-darabok, jó-e a keresés).
* **Faithfulness és Answer Relevancy:** A **generáló komponenst (nyelvi modellt)** minősíti (mennyire követi a promptot és a kontextust).
* **Answer Correctness:** Az **egész rendszert egyben** minősíti.

---

## 📂 A tesztfájlok felépítése és logikája

A projektben található fájlok jól szemléltetik, hogyan fejlődött a kiértékelési logika az egyszerűtől a hibatűrő, darabolt megközelítésig.

### 📑 Alapadatbázis (`tesztek.txt`)
Ez a fájl tartalmazza a kiértékelés alapját képező kérdés-válasz párokat. Ez biztosítja a **Ground Truth** (referencia) értékeket, amelyekhez a rendszer a generált válaszokat hasonlítja.

### 🛠️ A Python szkriptek működési logikája

1. **`RAGAS_test.py` (Az Alapértelmezett Csővezeték):**
   * **Mit tesztel:** Egy alap RAG folyamatot mér fel (beolvasás, darabolás, indexelés, generálás).
   * **Hogyan:** A dokumentumok feldolgozása és a válaszgenerálás után **egy menetben** futtatja le a kiértékelést. Egyszerűbb, alapszintű metrikákat használ, fix időzített várakozással a kérések között.

2. **`RAGAS_test2.py`, `RAGAS_test5.py` és `RAGAS_test6.py` (Keresés-finomítás és Elkülönített Mérés):**
   * **Mit tesztel:** A finomhangolt, újrarangsorolással (Reranking) kiegészített visszakeresést vizsgáztatja.
   * **Hogyan:** Beépít egy hibakezelő konfigurációt a hálózati hibák kivédésére. A `test5.py` még óvatosabb: a metrikákat nem egyszerre, hanem **külön-külön, egymás után** futtatja le, hogy csökkentse az egyidejű terhelést.

3. **`RAGAS_test3.py` és `RAGAS_test4.py` (Offline / Utólagos Kiértékelés):**
   * **Mit tesztel:** Kizárólag a kiértékelő algoritmust futtatja már meglévő adatokon.
   * **Hogyan:** Teljesen elválasztja a generálást a teszteléstől. Nem futtatja le újra a kereséseket, hanem egy korábban elmentett `results.json` fájlból tölti be a kérdéseket, kontextusokat és válaszokat, majd erre futtatja rá a mérést.

4. **`RAGAS_test7.py` (A Teljes, Kétlépcsős Batch Értékelő):**
   * **Mit tesztel:** A teljes mentett adatállományt értékeli ki két külön részletben, hogy megelőzze az időtúllépést és a szerver összeomlását.
   * **Hogyan:** Beolvassa a `results.json` tartalmát, majd egy futáson belül kettéosztja azt. Az első 25 kérdést kiértékeli és kimenti a `ragas_1_resz.csv` fájlba, majd közvetlenül utána a maradékot (25. elemtől) is feldolgozza, és elmenti a `ragas_2_resz.csv` fájlba.

5. **`RAGAS_test8.py` (Célzott Hibaelhárító / Mentőöv Szkript):**
   * **Mit tesztel:** Kizárólag az adathalmaz második felét (a 25. kérdéstől felfelé) teszteli.
   * **Hogyan:** Ez egy dedikált biztonsági szkript. Ha a `RAGAS_test7.py` futása közben a távoli szerver megszakadna, ezzel a szkripttel közvetlenül és önállóan is elindítható a második szakasz kiértékelése és mentése, így nem kell az első 25 kérdést újraértékelni.

---

## ⚠️ API szerver korlátok 

A kiértékelés rendkívül erőforrás-igényes, mivel a háttérben a kiértékelőnek számos részfeladatot kell elvégeznie (mondatok kinyerése, logikai állítások vizsgálata, összehasonlítások). Ez két fő hibaforráshoz vezet:

1. **`429 Too Many Requests` (Percenkénti limit túllépése):** Túl sok kérést küldünk túl rövid idő alatt.
2. **`503 Service Unavailable` (A szolgáltatás átmenetileg nem elérhető):** Ez egy szerveroldali hiba. Azt jelenti, hogy a távoli API szerver a hatalmas mennyiségű kérés miatt **teljesen túlterhelődött**, összeomlott, vagy szándékosan lezárta a kapcsolatot, mert nem bírja kiszolgálni a kért műveleteket.

### Hogyan védekeznek a kódok a túlterhelés és az 503-as hiba ellen?
* **Párhuzamosítás tiltása (`max_workers=1`):** Kényszeríti a rendszert, hogy szigorúan egymás után, ne pedig egyszerre küldje a mérési kéréseket, így nem bombázzuk a szervert.
* **Agresszív újrapróbálkozás és kényszerített kivárás (`max_retries=20`, `max_wait=120`):** Ha a szerver **503-as hibát** dob, a kód nem áll le hibával. A konfiguráció miatt a szkript észleli a leállást, tart egy kényszerpihenőt (akár 2 percet is), megvárja, amíg a távoli szerver fellélegzik, majd automatikusan újra megpróbálja elküldeni az adatokat (akár 20 alkalommal is).
* **Szakaszos mentés:** Az eredmények azonnali CSV-be írása biztosítja, hogy ha az 503-as hiba tartós maradna és a kód mégis leállna, a korábbi adatok ne vesszenek el.

---

## 🎯 Stratégiai Ajánlás: Melyik módszert érdemes alkalmazni?

Nagyobb vagy instabil API eléréssel rendelkező teszthalamok esetén a **RAGAS_test7.py és RAGAS_test8.py által képviselt kombinált, offline batch megközelítést** a legérdemesebb alkalmazni.

### Miért ez a legjobb választás?
* **Védelem az 503-as hiba miatti adatvesztés ellen:** A `test7.py` két külön blokkra bontva menti el a méréseket. Ha a szerver a folyamat vége felé kapna 503-as sokkot és megszakadna, a `ragas_1_resz.csv` már biztonságban megvan.
* **Azonnali javíthatóság:** Ha a szerver tartósan túlterheltté válik és a folyamat megszakad, a `test8.py` segítségével a szerver helyreállása után azonnal, a korábbi eredmények megismétlése nélkül folytatható a kiértékelés a 25. kérdéstől.
* **Költség- és időhatékonyság:** Mivel a már elmentett `results.json` fájlból dolgoznak, a tesztelés módosítása vagy újraindítása nem pazarolja az API erőforrásokat a válaszok felesleges újragenerálására.