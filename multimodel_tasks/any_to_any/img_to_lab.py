# Task 3: Image Classification (Image → Labels)
# Model: google/vit-base-patch16-224

from transformers import pipeline
from PIL import Image
import requests

classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

# Load image from URL (or use Image.open("your_image.jpg"))
url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)

results = classifier(image)

print("Top predictions:")
for r in results[:5]:
    print(f"  {r['label']:<30} {r['score']*100:.1f}%")