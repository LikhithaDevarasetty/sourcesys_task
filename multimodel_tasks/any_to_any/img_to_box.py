# Task 6: Object Detection (Image → Bounding Boxes)
# Model: facebook/detr-resnet-50

from transformers import DetrImageProcessor, DetrForObjectDetection
from PIL import Image, ImageDraw
import requests
import torch

processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

# Load image
url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw).convert("RGB")

inputs = processor(images=image, return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)

# Convert outputs to bounding boxes
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(
    outputs,
    target_sizes=target_sizes,
    threshold=0.9
)[0]

print("Detected objects:")
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    label_name = model.config.id2label[label.item()]
    box_coords = [round(i, 1) for i in box.tolist()]
    print(f"  {label_name:<20} confidence: {score:.2f}  box: {box_coords}")

# Draw boxes on image and save
draw = ImageDraw.Draw(image)
for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
    if score > 0.9:
        box = box.tolist()
        draw.rectangle(box, outline="red", width=3)
        draw.text((box[0], box[1] - 10), model.config.id2label[label.item()], fill="red")

image.save("detected_objects.jpg")
print("\nImage with bounding boxes saved to: detected_objects.jpg")