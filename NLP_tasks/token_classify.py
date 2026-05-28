from transformers import pipeline

# Load Token Classification Pipeline
classifier = pipeline(
    "token-classification",
    model="dbmdz/bert-large-cased-finetuned-conll03-english",
    aggregation_strategy="simple"
)

# Input Text
text = """
Barack Obama was born in Hawaii and worked at Microsoft in the United States.
"""

# Predict Entities
results = classifier(text)

# Print Results
print("Input Text:\n")
print(text)

print("\nDetected Entities:\n")

for result in results:
    
    print("Entity :", result["word"])
    print("Type   :", result["entity_group"])
    print("Score  :", result["score"])
    print("-" * 50)