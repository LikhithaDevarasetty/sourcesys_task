# Task 2: Visual Question Answering (Image + Text → Text)
# Model: Salesforce/blip-vqa-base

from transformers import BlipProcessor, BlipForQuestionAnswering
from PIL import Image
import requests

processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

# Load image
url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

# Ask questions about the image
questions = [
    "What animals are in the image?",
    "How many cats are there?",
    "What color is the sofa?",
]

for question in questions:
    inputs = processor(image, question, return_tensors="pt")
    output = model.generate(**inputs)
    answer = processor.decode(output[0], skip_special_tokens=True)
    print(f"Q: {question}")
    print(f"A: {answer}\n")