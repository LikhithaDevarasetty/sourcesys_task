from transformers import pipeline

# Load Translator
translator = pipeline(
    "translation_en_to_de",
    model="Helsinki-NLP/opus-mt-en-de"
)

# Input Sentence
text = "Artificial Intelligence is very powerful."

# Translate
result = translator(text)

# Print Result
print(result[0]["translation_text"])