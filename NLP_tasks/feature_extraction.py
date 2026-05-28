from transformers import pipeline
import torch
import numpy as np

# Load feature extraction pipeline
checkpoint = "facebook/bart-base"

feature_extractor = pipeline(
    "feature-extraction",
    model=checkpoint,
    framework="pt"
)

# Input text
text = "I enjoy Natural Language Processing tasks."

# Extract features
output = feature_extractor(text, return_tensors="pt")

# Convert to tensor
embeddings = output[0]

# Print tensor shape
print("Tensor Shape:", embeddings.shape)

# Mean pooling to get sentence embedding
sentence_embedding = embeddings.mean(dim=0)

print("\nSentence Embedding Shape:")
print(sentence_embedding.shape)

print("\nSentence Embedding:")
print(sentence_embedding)