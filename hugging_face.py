"""
NLP vs Hugging Face — Side-by-side Comparison
Tasks covered:
  1. Sentiment Analysis
  2. Named Entity Recognition (NER)
  3. Text Summarization (basic extractive vs abstractive)

Traditional NLP  → NLTK + spaCy
Hugging Face     → transformers (pipeline API)

Install deps first:
    pip install nltk spacy transformers torch
    python -m spacy download en_core_web_sm
    python -m nltk.downloader vader_lexicon punkt averaged_perceptron_tagger maxent_ne_chunker words
"""

import time
import textwrap

# ── shared sample text ────────────────────────────────────────────────────────

SAMPLE_SHORT = "The new iPhone release was absolutely fantastic and people loved it, " \
               "but the battery life was terrible and prices were way too high."

SAMPLE_LONG = (
    "Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in "
    "Cupertino, California in 1976. The company revolutionised the smartphone "
    "industry with the launch of the iPhone in 2007. Elon Musk, the CEO of Tesla "
    "and SpaceX, has frequently commented on Apple's dominance in the tech market. "
    "Microsoft, headquartered in Redmond, Washington, remains Apple's fiercest rival. "
    "In 2023, Apple became the first company to cross a market cap of three trillion dollars."
)


# ─────────────────────────────────────────────────────────────────────────────
# TASK 1 — SENTIMENT ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

def sentiment_nltk(text):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        label = "POSITIVE"
    elif compound <= -0.05:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"
    return label, round(compound, 4), scores


def sentiment_hf(text):
    from transformers import pipeline
    clf = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    result = clf(text[:512])[0]          # distilbert has a 512-token limit
    return result["label"], round(result["score"], 4)


# ─────────────────────────────────────────────────────────────────────────────
# TASK 2 — NAMED ENTITY RECOGNITION
# ─────────────────────────────────────────────────────────────────────────────

def ner_spacy(text):
    import spacy
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


def ner_hf(text):
    from transformers import pipeline
    ner = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english",
                   aggregation_strategy="simple")
    results = ner(text)
    entities = [(r["word"], r["entity_group"]) for r in results]
    return entities


# ─────────────────────────────────────────────────────────────────────────────
# TASK 3 — SUMMARIZATION
# (extractive with NLTK frequency scoring vs abstractive with HF BART)
# ─────────────────────────────────────────────────────────────────────────────

def summarize_nltk(text, top_n=2):
    """Frequency-based extractive summary — picks highest-scoring sentences."""
    import nltk
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from collections import Counter
    import string

    nltk.download("stopwords", quiet=True)
    stop_words = set(stopwords.words("english"))

    sentences = sent_tokenize(text)
    words = [w.lower() for w in word_tokenize(text)
             if w.lower() not in stop_words and w not in string.punctuation]
    freq = Counter(words)

    scores = {}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in freq:
                scores[sent] = scores.get(sent, 0) + freq[word]

    ranked = sorted(scores, key=scores.get, reverse=True)
    return " ".join(ranked[:top_n])


def summarize_hf(text):
    # "summarization" task alias was removed in newer transformers versions.
    # calling the model directly via its own classes avoids that issue entirely.
    from transformers import BartForConditionalGeneration, BartTokenizer

    model_name = "facebook/bart-large-cnn"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=60,
        min_length=20,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


# ─────────────────────────────────────────────────────────────────────────────
# RUNNER + PRETTY PRINTER
# ─────────────────────────────────────────────────────────────────────────────

def divider(title=""):
    width = 70
    if title:
        pad = (width - len(title) - 2) // 2
        print("\n" + "─" * pad + f" {title} " + "─" * pad)
    else:
        print("─" * width)


def wrap(text, indent=4):
    return textwrap.fill(str(text), width=66, initial_indent=" " * indent,
                         subsequent_indent=" " * indent)


def run_comparison():
    print("\n" + "=" * 70)
    print("    NLP (NLTK / spaCy)  vs  Hugging Face Transformers")
    print("=" * 70)

    # ── Task 1: Sentiment ──────────────────────────────────────────────────
    divider("TASK 1 · SENTIMENT ANALYSIS")
    print(f"\nInput: {SAMPLE_SHORT}\n")

    t0 = time.time()
    nltk_label, nltk_score, raw_scores = sentiment_nltk(SAMPLE_SHORT)
    nltk_time = time.time() - t0
    print(f"  [NLTK VADER]")
    print(f"    Label    : {nltk_label}")
    print(f"    Compound : {nltk_score}  (pos={raw_scores['pos']}, neg={raw_scores['neg']}, neu={raw_scores['neu']})")
    print(f"    Time     : {nltk_time:.3f}s\n")

    t0 = time.time()
    hf_label, hf_score = sentiment_hf(SAMPLE_SHORT)
    hf_time = time.time() - t0
    print(f"  [HuggingFace distilbert-sst2]")
    print(f"    Label    : {hf_label}")
    print(f"    Score    : {hf_score}")
    print(f"    Time     : {hf_time:.3f}s")

    print("\n  ── Notes ──")
    print("  VADER works via lexicon lookup — fast but misses nuance.")
    print("  distilBERT captures context (notices mixed sentiment better).")

    # ── Task 2: NER ───────────────────────────────────────────────────────
    divider("TASK 2 · NAMED ENTITY RECOGNITION")
    print(f"\nInput (first 80 chars): {SAMPLE_LONG[:80]}...\n")

    t0 = time.time()
    spacy_ents = ner_spacy(SAMPLE_LONG)
    spacy_time = time.time() - t0
    print(f"  [spaCy en_core_web_sm]")
    for text, label in spacy_ents:
        print(f"    {label:<12} → {text}")
    print(f"    Time: {spacy_time:.3f}s\n")

    t0 = time.time()
    hf_ents = ner_hf(SAMPLE_LONG)
    hf_time = time.time() - t0
    print(f"  [HuggingFace bert-large-conll03]")
    for text, label in hf_ents:
        print(f"    {label:<12} → {text}")
    print(f"    Time: {hf_time:.3f}s")

    print("\n  ── Notes ──")
    print("  spaCy is fast and good for production pipelines.")
    print("  BERT-large is slower but has higher F1, especially for rare entities.")

    # ── Task 3: Summarization ─────────────────────────────────────────────
    divider("TASK 3 · TEXT SUMMARIZATION")
    print(f"\nInput:\n{wrap(SAMPLE_LONG)}\n")

    t0 = time.time()
    nltk_summary = summarize_nltk(SAMPLE_LONG)
    nltk_time = time.time() - t0
    print(f"  [NLTK Extractive — frequency scoring]")
    print(wrap(nltk_summary))
    print(f"    Time: {nltk_time:.3f}s\n")

    t0 = time.time()
    hf_summary = summarize_hf(SAMPLE_LONG)
    hf_time = time.time() - t0
    print(f"  [HuggingFace BART-large-cnn — abstractive]")
    print(wrap(hf_summary))
    print(f"    Time: {hf_time:.3f}s")

    print("\n  ── Notes ──")
    print("  Extractive: lifts sentences directly — no hallucination risk.")
    print("  BART: paraphrases and fuses info — far more readable output.")

    # ── Final Comparison Table ────────────────────────────────────────────
    divider("OVERALL COMPARISON")
    rows = [
        ("Aspect",            "Traditional NLP",          "Hugging Face"),
        ("─" * 20,            "─" * 22,                   "─" * 22),
        ("Speed",             "Very fast (ms)",            "Slower (sec, GPU helps)"),
        ("Setup",             "Simple pip + download",     "Large model downloads"),
        ("Accuracy",          "Decent for basics",         "State-of-the-art"),
        ("Context awareness", "Limited / rule-based",      "Deep via attention"),
        ("Custom training",   "Manual feature eng.",       "Fine-tune pre-trained"),
        ("Resource use",      "Low RAM, CPU only",         "High RAM / needs GPU"),
        ("Best for",          "Production speed, rules",   "Research, accuracy"),
    ]
    for r in rows:
        print(f"  {r[0]:<22} {r[1]:<24} {r[2]}")

    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    run_comparison()