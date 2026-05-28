# Document Question Answering (Document Visual QA)
# Uses: microsoft/layoutlm-base-uncased (text + position + image features)
# Dataset: Downloads a sample document image automatically — no file needed!
#
# pip install transformers torch torchvision Pillow requests datasets

from transformers import pipeline
from PIL import Image
import requests
import os


# ── Load the Document QA pipeline ────────────────────────────────────────────

print("Loading Document QA model (impira/layoutlm-document-qa)...")
doc_qa = pipeline(
    "document-question-answering",
    model="impira/layoutlm-document-qa"
)
print("Model ready.\n")


# ── Load a sample document image ─────────────────────────────────────────────
# Using a publicly available invoice/receipt sample image

def get_sample_document():
    # Sample invoice image from Hugging Face datasets
    sample_url = "https://huggingface.co/spaces/impira/docquery/resolve/2359223c1837a7587402bda0f2643382a6eefeab/invoice.png"

    local_path = "sample_invoice.png"

    if not os.path.exists(local_path):
        print("Downloading sample invoice image...")
        response = requests.get(sample_url, stream=True)
        with open(local_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Saved to: {local_path}\n")
    else:
        print(f"Using cached: {local_path}\n")

    return Image.open(local_path)


# ── Ask questions about the document ─────────────────────────────────────────

def ask_document(image, questions):
    print("=" * 60)
    print("DOCUMENT QUESTION ANSWERING")
    print("=" * 60)

    for question in questions:
        result = doc_qa(image, question)

        # result is a list of answers sorted by confidence
        top = result[0] if isinstance(result, list) else result

        print(f"\nQ: {question}")
        print(f"A: {top['answer']}")
        print(f"   Confidence: {top['score']:.4f}")

    print("\n" + "=" * 60)


# ── Main ──────────────────────────────────────────────────────────────────────

image = get_sample_document()
print(f"Document image size: {image.size[0]}x{image.size[1]} pixels\n")

# Questions about the invoice
questions = [
    "What is the invoice number?",
    "What is the total amount due?",
    "What is the due date?",
    "Who is the invoice from?",
    "What is the tax amount?",
]

ask_document(image, questions)

print("\nTo use your OWN document image:")
print('  image = Image.open("your_document.jpg")  # or .png, .pdf page')
print('  ask_document(image, ["your question here"])')