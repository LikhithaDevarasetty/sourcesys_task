# 🧠 NLP Tasks Collection

A comprehensive collection of **12 essential Natural Language Processing (NLP) tasks** implemented in Python using the Hugging Face `transformers` library, `PyTorch`, and `pandas`. 

Each script in this repository is a standalone demonstration of a specific NLP pipeline, showcasing state-of-the-art pretrained models performing tasks ranging from text classification to table-based question answering.

---

## 🛠️ Installation & Setup

Before running any script, make sure you have Python installed. It is recommended to use a virtual environment.

### 1. Clone or Navigate to the Folder
```bash
cd NLP_tasks
```

### 2. Set Up a Virtual Environment (Optional but Recommended)
On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
You can install all dependencies at once using `requirements.txt`:
```bash
pip install -r requirements.txt
```

Alternatively, you can install the individual libraries one-by-one:
```bash
# Core machine learning & NLP libraries
pip install transformers torch

# Data processing libraries
pip install pandas numpy

# Additional helper packages for specialized models (e.g. translation)
pip install sentencepiece sacremoses
```

> [!NOTE]
> When running the scripts for the first time, Hugging Face will automatically download the required model weights (which may range from a few megabytes to several hundred megabytes). These will be cached locally for future offline executions.

---

## 📋 Task Directory & Overview

Here is an index of all NLP tasks included in this repository.

| # | Task | Script Name | Core Model | Libraries Used |
|---|------|-------------|------------|----------------|
| 1 | **Sentiment Analysis** | [`text_classify.py`](file:///c:/Users/kamal/OneDrive/sourcesys/NLP_tasks/text_classify.py) | `distilbert-base-uncased-finetuned-sst-2-english` | `transformers` |
| 2 | **Zero-Shot Classification** | [`zero_shot_classify.py`](file:///c:/Users/kamal/OneDrive/sourcesys/NLP_tasks/zero_shot_classify.py) | `facebook/bart-large-mnli` | `transformers` |
| 3 | **Named Entity Recognition (NER)** | [`token_classify.py`](file:///c:/Users/kamal/OneDrive/sourcesys/NLP_tasks/token_classify.py) | `dbmdz/bert-large-cased-finetuned-conll03-english` | `transformers` |
| 4 | **Question Answering** | [`Q_A.py`](file:///c:/Users/kamal/OneDrive/sourcesys/NLP_tasks/Q_A.py) | `distilbert-base-cased-distilled-squad` | `transformers` |
| 5 | **Table Question Answering** | [`table_Q_A.py`](file:///c:/Users/kamal/OneDrive/sourcesys/NLP_tasks/table_Q_A.py) | `google/tapas-base-finetuned-wtq` | `transformers`, `pandas` |
| 6 | **Text Summarization** | [`sumarization.py`](file:///c:/Users/kamal/OneDrive/sourcesys/NLP_tasks/sumarization.py) | `facebook/bart-large-cnn` | `transformers` |
| 7 | **Machine Translation** | [`translation.py`](file:///c:/Users/kamal/OneDrive/sourcesys/NLP_tasks/translation.py) | `Helsinki-NLP/opus-mt-en-de` | `transformers` |
| 8 | **Text Generation** | [`text_gen.py`](file:///c:/Users/kamal/OneDrive/sourcesys/NLP_tasks/text_gen.py) | `gpt2` | `transformers` |
| 9 | **Masked Language Modeling** | [`fill_mask.py`](file:///c:/Users/kamal/OneDrive/sourcesys/NLP_tasks/fill_mask.py) | `bert-base-uncased`, `roberta-base`, `distilbert-base` | `transformers` |
| 10 | **Feature Extraction** | [`feature_extraction.py`](file:///c:/Users/kamal/OneDrive/sourcesys/NLP_tasks/feature_extraction.py) | `facebook/bart-base` | `transformers`, `torch`, `numpy` |
| 11 | **Sentence Similarity** | [`Sentence_similarity.py`](file:///c:/Users/kamal/OneDrive/sourcesys/NLP_tasks/Sentence_similarity.py) | `bert-base-uncased` | `transformers`, `torch` |
| 12 | **Text Re-Ranking** | [`text_ranking.py`](file:///c:/Users/kamal/OneDrive/sourcesys/NLP_tasks/text_ranking.py) | `cross-encoder/ms-marco-MiniLM-L-6-v2` | `transformers` |

---

## 🔍 Detailed Walkthrough of Every Task

---

### 1. Sentiment Analysis (`text_classify.py`)
* **Explanation**: Analyzes input text to determine the sentiment (e.g. positive, negative) and assigns a confidence score.
* **How it works**: Uses a pre-trained DistilBERT model optimized for binary sentiment classification on the SST-2 dataset.
* **Execution**:
  ```bash
  python text_classify.py
  ```
* **Sample Output**:
  ```text
  Text : I love machine learning.
  Prediction : POSITIVE
  Score : 0.9998
  --------------------------------------------------
  Text : This movie was terrible.
  Prediction : NEGATIVE
  Score : 0.9997
  ...
  ```

---

### 2. Zero-Shot Classification (`zero_shot_classify.py`)
* **Explanation**: Classifies input text into a set of custom, user-defined labels on-the-fly, without needing any task-specific training data.
* **How it works**: Leverages Natural Language Inference (NLI) with a large BART model to evaluate how well a sentence matches candidate hypothesis labels.
* **Execution**:
  ```bash
  python zero_shot_classify.py
  ```
* **Sample Output**:
  ```text
  Text:
  Transformers models are widely used in Natural Language Processing tasks.

  Predicted Labels:

  Label : technology
  Score : 0.9856
  Label : education
  Score : 0.0102
  Label : health
  Score : 0.0023
  Label : sports
  Score : 0.0019
  ```

---

### 3. Named Entity Recognition - NER (`token_classify.py`)
* **Explanation**: Extracts entities (such as people, organizations, locations) from unstructured text and tags each one with its respective type.
* **How it works**: Employs a token-classification pipeline on a fine-tuned BERT model, using aggregation to group word-pieces back into full terms.
* **Execution**:
  ```bash
  python token_classify.py
  ```
* **Sample Output**:
  ```text
  Detected Entities:

  Entity : Barack Obama
  Type   : PER
  Score  : 0.9987
  --------------------------------------------------
  Entity : Hawaii
  Type   : LOC
  Score  : 0.9972
  --------------------------------------------------
  Entity : Microsoft
  Type   : ORG
  ...
  ```

---

### 4. Question Answering (`Q_A.py`)
* **Explanation**: Extracts answers from a given reference context in response to a natural language query (extractive QA).
* **How it works**: Scans the context block to identify the exact character span that contains the answer using a SQuAD-trained DistilBERT.
* **Execution**:
  ```bash
  python Q_A.py
  ```
* **Sample Output**:
  ```text
  Question: When was Hugging Face founded?
  Answer: 2016
  ```

---

### 5. Table Question Answering (`table_Q_A.py`)
* **Explanation**: Formulates queries against structural tabular data, allowing you to ask questions about rows, columns, averages, or specific records.
* **How it works**: Uses TAPAS (Table Parser) which processes a Pandas DataFrame and a question text, outputting cell coordinates and aggregate answers.
* **Libraries**: `pandas`, `transformers`
* **Execution**:
  ```bash
  python table_Q_A.py
  ```
* > [!IMPORTANT]
  > TAPAS expects all structural numbers and entries in the DataFrame to be represented strictly as **strings** rather than raw floats or integers.
* **Sample Output**:
  ```text
  Question : What is the salary of Bob?
  Answer   : 80000
  --------------------------------------------------
  Question : Who works in Engineering?
  Answer   : Bob, Diana
  --------------------------------------------------
  Question : What is the average salary?
  Answer   : AVERAGE > 50000, 80000, 60000, 75000
  ```

---

### 6. Text Summarization (`sumarization.py`)
* **Explanation**: Summarizes a long paragraph or document into a concise and readable sentence while maintaining key context.
* **How it works**: Uses a sequence-to-sequence BART model fine-tuned on the CNN/DailyMail dataset to perform abstractive/extractive summarization.
* **Execution**:
  ```bash
  python sumarization.py
  ```
* **Sample Output**:
  ```text
  Original Text:
  Artificial Intelligence is transforming the world rapidly. Machine learning and deep learning are subsets of AI...

  Summary:
  Artificial Intelligence is transforming the world rapidly. Machine learning and deep learning are subsets of AI. Hugging Face provides pretrained transformer models for various NLP tasks.
  ```

---

### 7. Machine Translation (`translation.py`)
* **Explanation**: Translates text from a source language (English) to a target language (German).
* **How it works**: Employs a MarianMT sequence-to-sequence model trained on the OPUS multilingual parallel corpus.
* **Execution**:
  ```bash
  python translation.py
  ```
* **Sample Output**:
  ```text
  Künstliche Intelligenz ist sehr leistungsfähig.
  ```

---

### 8. Text Generation (`text_gen.py`)
* **Explanation**: Auto-completes or generates creative passages starting from an initial text prompt.
* **How it works**: Uses an autoregressive language model (GPT-2) to iteratively predict the most likely subsequent words.
* **Execution**:
  ```bash
  python text_gen.py
  ```
* **Sample Output**:
  ```text
  Generated Text:

  Artificial Intelligence is a dynamic field of research with a lot of potential applications in a number of fields, from engineering to manufacturing, and we have many of them.
  ```

---

### 9. Masked Language Modeling - Fill Mask (`fill_mask.py`)
* **Explanation**: Solves "fill-in-the-blank" puzzles by predicting what word fits best in a designated masked position.
* **How it works**: Compares three foundation models: **BERT** (`[MASK]`), **RoBERTa** (`<mask >`), and **DistilBERT** (`[MASK]`), demonstrating how different architectures predict missing vocabulary.
* **Execution**:
  ```bash
  python fill_mask.py
  ```
* **Sample Output**:
  ```text
  BERT Predictions:
  machine learning is key .
  machine learning is great .
  machine learning is difficult .

  RoBERTa Predictions:
  machine learning is hard .
  machine learning is key .
  machine learning is easy .
  ```

---

### 10. Feature Extraction (`feature_extraction.py`)
* **Explanation**: Extracts numerical vector representations (embeddings) from input text. These representations are suitable for downstream ML tasks like classification, clustering, or indexing.
* **How it works**: Extracts raw hidden states from a pre-trained BART model and applies PyTorch mean-pooling to derive a single 768-dimensional sentence embedding vector.
* **Libraries**: `torch`, `numpy`, `transformers`
* **Execution**:
  ```bash
  python feature_extraction.py
  ```
* **Sample Output**:
  ```text
  Tensor Shape: torch.Size([9, 768])

  Sentence Embedding Shape:
  torch.Size([768])

  Sentence Embedding:
  tensor([-0.1203,  0.0842,  0.5123,  ...,  0.0381])
  ```

---

### 11. Sentence Similarity (`Sentence_similarity.py`)
* **Explanation**: Compares two sentences to measure how semantically similar they are on a scale of -1 to 1.
* **How it works**: Extracts raw token embeddings from `bert-base-uncased`, calculates the mean-pooled vector representing each sentence, and then evaluates the Cosine Similarity between them.
* **Libraries**: `torch`, `transformers`
* **Execution**:
  ```bash
  python Sentence_similarity.py
  ```
* **Sample Output**:
  ```text
  Sentence 1 : Machine learning is amazing
  Sentence 2 : Artificial intelligence is fascinating

  Similarity Score :
  0.8654219150543213
  ```

---

### 12. Text Re-Ranking (`text_ranking.py`)
* **Explanation**: Evaluates the semantic relevance of several target passages against an input query, re-ranking them from most relevant to least relevant.
* **How it works**: Employs a Cross-Encoder (`ms-marco-MiniLM-L-6-v2`) which processes the query and document jointly through attention heads to compute a unified relevancy score.
* **Execution**:
  ```bash
  python text_ranking.py
  ```
* **Sample Output**:
  ```text
  Query:
  What is Artificial Intelligence?

  Ranked Documents:

  Rank 1
  Document : Artificial Intelligence is the simulation of human intelligence by machines.
  Score    : 0.99824
  --------------------------------------------------
  Rank 2
  Document : Machine learning is a subset of Artificial Intelligence.
  Score    : 0.81232
  --------------------------------------------------
  Rank 3
  ...
  ```

---

## 🚀 Summary of Best Practices Shown
1. **Pipeline Optimization**: Showcases Hugging Face `pipeline` utilities for rapid deployment.
2. **Framework Specification**: Explicitly manages PyTorch tensors using `framework="pt"` and `.return_tensors="pt"`.
3. **Pooling Strategies**: Demonstrates how to pool raw contextual embeddings (using `mean(dim=0)`) to get unified sentence-level embeddings.
4. **Cross-Encoders**: Shows the proper formatting of cross-encoder queries using `[SEP]` separators for state-of-the-art search re-ranking.
