from transformers import pipeline
from PIL import Image

# ── INPUTS ──────────────────────────────────────
IMAGE_PATH = "image-text-to-video-input.jpg"
QUESTION   = "What is in this image?"
# ────────────────────────────────────────────────

print("Loading VQA model...")
vqa = pipeline("visual-question-answering", model="dandelin/vilt-b32-finetuned-vqa")

image = Image.open(IMAGE_PATH).convert("RGB")

print(f"\nQuestion : {QUESTION}")
print("-" * 40)

results = vqa(image, QUESTION, top_k=5)

print(f"{'Answer':<20} {'Score':>8}")
print("-" * 40)
for r in results:
    bar = "█" * int(r["score"] * 30)
    print(f"{r['answer']:<20} {r['score']:>6.3f}  {bar}")

print("-" * 40)
print(f"\nTop Answer → {results[0]['answer']}  ({results[0]['score']:.3f})")