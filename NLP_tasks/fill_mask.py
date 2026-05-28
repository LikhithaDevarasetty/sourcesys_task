from transformers import pipeline

# -----------------------------
# BERT MODEL
# -----------------------------
bert = pipeline(
    "fill-mask",
    model="bert-base-uncased"
)

text_bert = "Machine learning is [MASK]."

print("\nBERT Predictions:\n")

bert_results = bert(text_bert)

for result in bert_results:
    print(result["sequence"])


# -----------------------------
# RoBERTa MODEL
# -----------------------------
roberta = pipeline(
    "fill-mask",
    model="roberta-base"
)

text_roberta = "Machine learning is <mask>."

print("\nRoBERTa Predictions:\n")

roberta_results = roberta(text_roberta)

for result in roberta_results:
    print(result["sequence"])


# -----------------------------
# DistilBERT MODEL
# -----------------------------
distilbert = pipeline(
    "fill-mask",
    model="distilbert-base-uncased"
)

text_distilbert = "Machine learning is [MASK]."

print("\nDistilBERT Predictions:\n")

distilbert_results = distilbert(text_distilbert)

for result in distilbert_results:
    print(result["sequence"])