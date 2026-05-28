from transformers import pipeline

# Load Text Classification Pipeline
ranker = pipeline(
    "text-classification",
    model="cross-encoder/ms-marco-MiniLM-L-6-v2"
)

# Query
query = "What is Artificial Intelligence?"

# Candidate Texts
documents = [
    "Artificial Intelligence is the simulation of human intelligence by machines.",
    
    "Cricket is one of the most popular sports in the world.",
    
    "Machine learning is a subset of Artificial Intelligence.",
    
    "Transformers models are widely used in NLP tasks."
]

# Rank Documents
results = []

for doc in documents:
    
    text = query + " [SEP] " + doc
    
    score = ranker(text)[0]["score"]
    
    results.append((doc, score))

# Sort by score
results = sorted(
    results,
    key=lambda x: x[1],
    reverse=True
)

# Print Ranked Results
print("Query:\n")
print(query)

print("\nRanked Documents:\n")

for rank, (doc, score) in enumerate(results, start=1):
    
    print(f"Rank {rank}")
    print("Document :", doc)
    print("Score    :", score)
    print("-" * 50)