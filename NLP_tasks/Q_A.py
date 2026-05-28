from transformers import pipeline

# Load the QA pipeline
qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Give it some context
context = """
Hugging Face is a company that builds tools for machine learning.
It was founded in 2016 and is based in New York. 
They created the Transformers library which is widely used for NLP tasks.
"""

# Ask a question
question = "When was Hugging Face founded?"

# Get the answer
result = qa(question=question, context=context)

print("Question:", question)
print("Answer:", result["answer"])