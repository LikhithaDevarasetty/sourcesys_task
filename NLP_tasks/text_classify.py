from transformers import pipeline

# Create classifier
classifier = pipeline(
    "sentiment-analysis"
)

# Texts
texts = [
    "I love machine learning.",
    "This movie was terrible.",
    "The project is very interesting."
]

# Predict sentiments
results = classifier(texts)

# Display results
for text, result in zip(texts, results):
    print("Text :", text)
    print("Prediction :", result["label"])
    print("Score :", result["score"])
    print("-" * 50)