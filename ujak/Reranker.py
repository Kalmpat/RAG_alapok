from sentence_transformers import CrossEncoder

def reranker(query, content):
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    all_pairs = [(query, con) for con in content]
    #print(all_pairs)
    scores = model.predict(all_pairs)
    #print("Eredmények", scores)
    best= max(scores)
    best_content = scores.tolist().index(best)
    #print(max_content)
    #print(all_pairs[best_content][1])
    #print(max)
    return all_pairs[best_content][1]


query = "How many people live in Berlin?"
content = ["Berlin had a population of 3,520,031 registered inhabitants in an area of 891.82 square kilometers.", "Berlin is well known for its museums."]
print(reranker(query, content))

