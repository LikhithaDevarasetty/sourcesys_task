from transformers import pipeline
import torch
from torch.nn.functional import cosine_similarity

# Load feature extraction pipeline
extractor = pipeline(
    "feature-extraction",
    model="bert-base-uncased"
)

# Sentences
sentence1 = "Machine learning is amazing"
sentence2 = "Artificial intelligence is fascinating"

# Extract embeddings
embedding1 = extractor(sentence1, return_tensors="pt")[0]
embedding2 = extractor(sentence2, return_tensors="pt")[0]

# Mean pooling
sentence_embedding1 = embedding1.mean(dim=0)
sentence_embedding2 = embedding2.mean(dim=0)

# Cosine similarity
similarity = cosine_similarity(
    sentence_embedding1,
    sentence_embedding2,
    dim=0
)

# Print similarity score
print("Sentence 1 :", sentence1)
print("Sentence 2 :", sentence2)

print("\nSimilarity Score :")
print(similarity.item())