import pandas as pd
from transformers import pipeline

# Load the table QA pipeline
table_qa = pipeline("table-question-answering", model="google/tapas-base-finetuned-wtq")

# IMPORTANT: All column names and values must be strings for TAPAS to work
data = {
    "Name":       ["Alice", "Bob", "Charlie", "Diana"],
    "Age":        ["25", "30", "35", "28"],
    "Department": ["HR", "Engineering", "Marketing", "Engineering"],
    "Salary":     ["50000", "80000", "60000", "75000"],
}

table = pd.DataFrame(data)

print("Table:")
print(table)
print()

# Ask questions
questions = [
    "What is the salary of Bob?",
    "Who works in Engineering?",
    "What is the average salary?",
    "Who is the oldest person?",
]

for question in questions:
    result = table_qa(table=table, query=question)
    print(f"Question : {question}")
    print(f"Answer   : {result['answer']}")
    print("-" * 50)