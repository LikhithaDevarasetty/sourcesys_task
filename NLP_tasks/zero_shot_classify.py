from transformers import pipeline

# Load Zero-Shot Classification Pipeline
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# Input Text
text = """
Transformers models are widely used in Natural Language Processing tasks.
"""

# Candidate Labels
labels = [
    "technology",
    "sports",
    "health",
    "education"
]

# Predict Labels
result = classifier(
    text,
    candidate_labels=labels
)

# Print Input
print("Text:\n")
print(text)

# Print Predictions
print("\nPredicted Labels:\n")

for label, score in zip(result["labels"], result["scores"]):
    
    print("Label :", label)
    print("Score :", score)
    print("-" * 50)