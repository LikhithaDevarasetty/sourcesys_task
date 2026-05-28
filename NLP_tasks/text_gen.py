from transformers import pipeline

# Load Text Generation Pipeline
generator = pipeline(
    "text-generation",
    model="gpt2"
)

# Input Prompt
prompt = "Artificial Intelligence is"

# Generate Text
result = generator(
    prompt,
    max_length=50,
    num_return_sequences=1
)

# Print Generated Text
print("Generated Text:\n")
print(result[0]["generated_text"])