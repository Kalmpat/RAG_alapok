import streamlit as st
from streamlit_image_zoom import image_zoom
from PIL import Image  # <--- Ez kell a kép megnyitásához

# 1. Kép megnyitása a Pillow-val
image_path = "images/home_ai.png"
img_object = Image.open(image_path)

st.title("Kép nagyítása teszt")

# 2. Most már az objektumot adjuk át, nem a fájlnevet
image_zoom(img_object, mode="scroll")

st.caption("Most már működnie kell a görgetős zoomnak!")