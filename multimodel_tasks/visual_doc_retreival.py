"""
Simple Visual Document Retrieval
Install: pip install colpali-engine transformers torch pillow pymupdf
"""

import torch
import fitz  # PyMuPDF
from PIL import Image
from colpali_engine.models import ColPali, ColPaliProcessor

# ── 1. Your inputs ──────────────────────────────────
PDF_PATH = "file-sample_150kB.pdf"
QUESTION = "Is the model in this paper the fastest for inference?"
TOP_K    = 3
# ────────────────────────────────────────────────────


# Load model
print("Loading model...")
device    = "cuda" if torch.cuda.is_available() else "cpu"
model     = ColPali.from_pretrained("vidore/colpali-v1.2", torch_dtype=torch.float32).eval().to(device)
processor = ColPaliProcessor.from_pretrained("vidore/colpali-v1.2")
print("Model ready.\n")

# PDF → images
doc    = fitz.open(PDF_PATH)
pages  = []
matrix = fitz.Matrix(150 / 72, 150 / 72)
for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=matrix)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    pages.append(img)
    print(f"  Loaded page {i+1}/{len(doc)}", end="\r")
print(f"\nLoaded {len(pages)} pages.\n")

# Encode pages
with torch.no_grad():
    inputs    = processor.process_images(pages)
    inputs    = {k: v.to(device) for k, v in inputs.items()}
    page_embs = model(**inputs).cpu()

# Encode query
with torch.no_grad():
    q_inputs  = processor.process_queries([QUESTION])
    q_inputs  = {k: v.to(device) for k, v in q_inputs.items()}
    query_emb = model(**q_inputs).cpu()

# Score & rank
scores = processor.score_multi_vector(query_emb, page_embs)[0].tolist()
ranked = sorted(enumerate(scores), key=lambda x: -x[1])

# Print results
print("=" * 50)
print("VISUAL DOCUMENT RETRIEVAL")
print("=" * 50)
print(f"Question: {QUESTION}\n")
for rank, (idx, score) in enumerate(ranked[:TOP_K], 1):
    print(f"  #{rank}  Page {idx+1:<5}  Score: {score:.3f}")
print("=" * 50)