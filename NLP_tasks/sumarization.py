from transformers import pipeline

# Load Summarization Pipeline
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

# Input Text
text = """
Artificial Intelligence is transforming the world rapidly.
Machine learning and deep learning are subsets of AI.
These technologies are used in healthcare, education,
finance, robotics, self-driving cars, and many other fields.
Hugging Face provides pretrained transformer models
for various NLP tasks like summarization, translation,
question answering, and text generation.
"""

# Generate Summary
summary = summarizer(
    text,
    max_length=50,
    min_length=20,
    do_sample=False
)

# Print Summary
print("Original Text:\n")
print(text)

print("\nSummary:\n")
print(summary[0]["summary_text"])