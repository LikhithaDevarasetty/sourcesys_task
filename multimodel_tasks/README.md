# 🌟 Multimodal AI Tasks Repository 🌟

Welcome to the **Multimodal AI Tasks Repository**! This project contains a diverse collection of state-of-the-art multimodal artificial intelligence pipelines built using the **Hugging Face Transformers** ecosystem, **PyTorch**, **Diffusers**, and other modern AI libraries. 

These tasks span across different modalities including **Text**, **Speech/Audio**, **Image**, **Video**, and **Document Visual QA**. Many of the scripts are designed to automatically download sample data (audios, images, PDFs), making them immediately runnable without any tedious pre-configuration.

---

## 📋 Table of Contents
1. [🛠️ Getting Started & Environment Setup](#%EF%B8%8F-getting-started--environment-setup)
2. [📦 Unified Dependency Installation](#-unified-dependency-installation)
3. [📂 Repository Structure](#-repository-structure)
4. [🚀 Detailed Task Guide (Root Folder)](#-detailed-task-guide-root-folder)
   - [1. Audio & Question Answering (`audio_text_to_text.py`)](#1-audio--question-answering-audio_text_to_textpy)
   - [2. Document Visual QA (`doc_que_ans.py`)](#2-document-visual-qa-doc_que_anspy)
   - [3. Image to Video Generation (`image_text_to_video.py`)](#3-image-to-video-generation-image_text_to_videopy)
   - [4. Visual Question Answering BLIP (`img_text_to_text.py`)](#4-visual-question-answering-blip-img_text_to_textpy)
   - [5. Video Captioning & QA (`video_text_to_text.py`)](#5-video-captioning--qa-video_text_to_textpy)
   - [6. Visual Document Retrieval ColPali (`visual_doc_retreival.py`)](#6-visual-document-retrieval-colpali-visual_doc_retreivalpy)
   - [7. Visual QA ViLT (`visual_que_ans.py`)](#7-visual-qa-vilt-visual_que_anspy)
5. [🔄 Detailed Task Guide (Any-to-Any Subdirectory)](#-detailed-task-guide-any-to-any-subdirectory)
   - [8. Speech-to-Text Transcribing (`any_to_any/audio_to_text.py`)](#8-speech-to-text-transcribing-any_to_anyaudio_to_textpy)
   - [9. Image Captioning (`any_to_any/image_to_text.py`)](#9-image-captioning-any_to_anyimage_to_textpy)
   - [10. Object Detection (`any_to_any/img_to_box.py`)](#10-object-detection-any_to_anyimg_to_boxpy)
   - [11. Image Classification (`any_to_any/img_to_lab.py`)](#11-image-classification-any_to_anyimg_to_labpy)
   - [12. Text-to-Speech synthesis (`any_to_any/text_to_audio.py`)](#12-text-to-speech-synthesis-any_to_anytext_to_audiopy)
6. [⚠️ Troubleshooting & Notes](#%EF%B8%8F-troubleshooting--notes)

---

## 🛠️ Getting Started & Environment Setup

Since this project is running on **Windows**, we recommend setting up a virtual environment (`venv`) to keep dependencies isolated and clean.

### 1. Create a Virtual Environment
Open your PowerShell or Command Prompt in the repository folder and run:
```powershell
python -m venv venv
```

### 2. Activate the Virtual Environment
* **PowerShell**:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
* **Command Prompt**:
  ```cmd
  .\venv\Scripts\activate.bat
  ```

---

## 📦 Unified Dependency Installation

If you want to install **every single dependency** required across all scripts in the entire workspace at once, execute the following command:

```bash
pip install torch torchvision torchaudio transformers diffusers colpali-engine pymupdf Pillow requests datasets opencv-python soundfile accelerate
```

> [!NOTE]
> * **CUDA Support**: If you have a compatible Nvidia GPU, you should install the GPU-compatible version of PyTorch first to speed up deep learning models (especially video and diffusion models) by following the instructions on the [PyTorch official website](https://pytorch.org/).
> * **OCR Engine**: Document visual QA (`doc_que_ans.py`) utilizes LayoutLM which may require system-level installation of **Tesseract OCR** for certain images.

---

## 📂 Repository Structure

```directory
multimodel_tasks/
│
├── any_to_any/                             # Folder containing core single-modal to single-modal tasks
│   ├── audio_to_text.py                    # Speech Recognition
│   ├── image_to_text.py                    # Image Captioning
│   ├── img_to_box.py                       # Object Detection & Bounding Boxes
│   ├── img_to_lab.py                       # Image Classification
│   └── text_to_audio.py                    # Text-to-Speech
│
├── audio_text_to_text.py                   # Speech Recognition + Question Answering
├── doc_que_ans.py                          # Document Visual QA pipeline
├── image_text_to_video.py                  # Stable Video Diffusion pipeline
├── img_text_to_text.py                     # Visual QA (BLIP)
├── video_text_to_text.py                   # Video Captioning & QA (LLaVA-NeXT)
├── visual_doc_retreival.py                 # PDF Visual Document Retrieval (ColPali)
└── visual_que_ans.py                       # Visual QA (ViLT)
```

---

## 🚀 Detailed Task Guide (Root Folder)

### 1. Audio & Question Answering (`audio_text_to_text.py`)
* **Brief Intro**: This task demonstrates a chain of two models: it first transcribes a speech segment into text, and then uses a Question Answering (QA) model to answer questions about the contents of the transcript. It automatically downloads a small sample audio (~1MB) from the LibriSpeech dataset so you do not need any local files to run it.
* **Libraries Used**: `torch`, `torchaudio`, `transformers`, `soundfile`
* **Pip Installation**:
  ```bash
  pip install torch torchaudio transformers soundfile
  ```
* **Models Used**:
  * Speech-to-Text: `facebook/wav2vec2-base-960h`
  * Question Answering: `deepset/roberta-base-squad2`
* **How to Run**:
  ```bash
  python audio_text_to_text.py
  ```
* **Expected Output**:
  * Information on the downloaded LibriSpeech audio.
  * Transcribed text.
  * Extracted text answers to the questions: *"What is being talked about?"*, *"What action is mentioned?"*, and *"Who or what is the subject?"*.

---

### 2. Document Visual QA (`doc_que_ans.py`)
* **Brief Intro**: Performs Document Visual Question Answering (DocVQA) on images of documents (e.g., invoices, forms, receipts). It reads both the visual layout and text semantics. By default, it downloads a sample invoice receipt image from Hugging Face and caches it locally as `sample_invoice.png`.
* **Libraries Used**: `transformers`, `torch`, `torchvision`, `Pillow`, `requests`, `datasets`
* **Pip Installation**:
  ```bash
  pip install transformers torch torchvision Pillow requests datasets
  ```
* **Models Used**: `impira/layoutlm-document-qa` (LayoutLM)
* **How to Run**:
  ```bash
  python doc_que_ans.py
  ```
* **Expected Output**:
  * Document dimensions and download logs.
  * Accurate answers extracted directly from the document image for questions about: Invoice number, Total amount due, Due date, Sender info, and Tax amount, alongside confidence scores.

---

### 3. Image to Video Generation (`image_text_to_video.py`)
* **Brief Intro**: Generates video frames starting from a single static input image using a diffusion pipeline.
* **Libraries Used**: `diffusers`, `Pillow`, `torch`, `accelerate`
* **Pip Installation**:
  ```bash
  pip install diffusers Pillow torch accelerate
  ```
* **Models Used**: `stabilityai/stable-video-diffusion-img2vid-xt`
* **How to Run**:
  ```bash
  python image_text_to_video.py
  ```
* **Expected Output**:
  * Saves a set of generated video frames and outputs: `Video Frames Generated`.
* **⚠️ Essential Code Fix Notice**: The code expects a local file named `image-text-to-video-input.png`. Since the folder actually contains `image-text-to-video-input.jpg`, you should update line 14 of the script from `image-text-to-video-input.png` to `image-text-to-video-input.jpg` before running, or rename the file.

---

### 4. Visual Question Answering BLIP (`img_text_to_text.py`)
* **Brief Intro**: Given an image (downloaded from COCO dataset URL) and a series of text questions, this script answers the questions based on the visual context of the image.
* **Libraries Used**: `transformers`, `Pillow`, `requests`, `torch`
* **Pip Installation**:
  ```bash
  pip install transformers Pillow requests torch
  ```
* **Models Used**: `Salesforce/blip-vqa-base` (BLIP)
* **How to Run**:
  ```bash
  python img_text_to_text.py
  ```
* **Expected Output**:
  * Predictions answering visual questions such as: *"What animals are in the image?"* (Expected: cats), *"How many cats are there?"* (Expected: 2), and *"What color is the sofa?"* (Expected: gray/stripes).

---

### 5. Video Captioning & QA (`video_text_to_text.py`)
* **Brief Intro**: Connects a video model to text generation. It reads video frames from a local video file (`input.mp4`) and generates a textual description answering what is happening in the video.
* **Libraries Used**: `transformers`, `torch`, `opencv-python` (cv2), `numpy`, `accelerate`
* **Pip Installation**:
  ```bash
  pip install transformers torch opencv-python numpy accelerate
  ```
* **Models Used**: `llava-hf/LLaVA-NeXT-Video-7B-hf`
* **How to Run**:
  ```bash
  python video_text_to_text.py
  ```
* **Expected Output**:
  * Decoded description of the events taking place in `input.mp4`.
* **⚠️ Hardware Requirement**: This script utilizes a 7-Billion parameter LLaVA-NeXT model and requires a GPU (CUDA) with sufficient VRAM.

---

### 6. Visual Document Retrieval ColPali (`visual_doc_retreival.py`)
* **Brief Intro**: Implements state-of-the-art visual document retrieval. Instead of doing expensive text extraction (OCR) and text search, it indexes PDF pages directly as visual vector embeddings using ColPali. It then ranks the PDF pages that best answer a visual search query.
* **Libraries Used**: `colpali-engine`, `transformers`, `torch`, `Pillow`, `pymupdf` (imported as `fitz`)
* **Pip Installation**:
  ```bash
  pip install colpali-engine transformers torch Pillow pymupdf
  ```
* **Models Used**: `vidore/colpali-v1.2`
* **How to Run**:
  ```bash
  python visual_doc_retreival.py
  ```
* **Expected Output**:
  * Renders pages from the PDF file `file-sample_150kB.pdf` into PIL images.
  * Encodes and ranks the pages matching the question: *"Is the model in this paper the fastest for inference?"*.
  * Prints a ranked list of page indexes along with similarity scores.

---

### 7. Visual QA ViLT (`visual_que_ans.py`)
* **Brief Intro**: Uses the Vision-and-Language Transformer (ViLT) pipeline to answer a visual query on a local image (`image-text-to-video-input.jpg`).
* **Libraries Used**: `transformers`, `Pillow`, `torch`
* **Pip Installation**:
  ```bash
  pip install transformers Pillow torch
  ```
* **Models Used**: `dandelin/vilt-b32-finetuned-vqa`
* **How to Run**:
  ```bash
  python visual_que_ans.py
  ```
* **Expected Output**:
  * A beautifully rendered CLI table containing the top 5 predicted answers, their confidence scores, and horizontal ASCII bar charts representing confidence levels. E.g.:
    ```
    Answer                  Score
    ----------------------------------------
    cat                     0.852  █████████████████████████
    ...
    ```

---

## 🔄 Detailed Task Guide (Any-to-Any Subdirectory)

All scripts in this section reside inside the `any_to_any/` folder. Make sure to navigate inside it (`cd any_to_any`) before running them or reference them with their subdirectory prefix.

### 8. Speech-to-Text Transcribing (`any_to_any/audio_to_text.py`)
* **Brief Intro**: Automatically downloads 3 test samples from the LibriSpeech dataset, converts them, and runs full Automatic Speech Recognition (ASR) to transcribe the speech into text.
* **Libraries Used**: `torch`, `torchaudio`, `transformers`, `soundfile`
* **Pip Installation**:
  ```bash
  pip install torch torchaudio transformers soundfile
  ```
* **Models Used**: `facebook/wav2vec2-base-960h`
* **How to Run**:
  ```bash
  python any_to_any/audio_to_text.py
  ```
* **Expected Output**:
  * Logs matching downloading and loading the models and dataset.
  * Formatted output displaying: Sample number, Speaker ID, Duration in seconds, Ground Truth (original script transcript), and Model Output (transcription text) for side-by-side comparison.

---

### 9. Image Captioning (`any_to_any/image_to_text.py`)
* **Brief Intro**: Generates natural language descriptive captions for a given image loaded from a COCO dataset URL.
* **Libraries Used**: `transformers`, `Pillow`, `requests`, `torch`
* **Pip Installation**:
  ```bash
  pip install transformers Pillow requests torch
  ```
* **Models Used**: `nlpconnect/vit-gpt2-image-captioning` (Vision Transformer encoder + GPT2 decoder)
* **How to Run**:
  ```bash
  python any_to_any/image_to_text.py
  ```
* **Expected Output**:
  * Generates and prints a clean description caption, for example: `Caption: a cat laying on top of a couch next to another cat`

---

### 10. Object Detection (`any_to_any/img_to_box.py`)
* **Brief Intro**: Detects objects in an image, extracts their classes and coordinates, draws colored bounding boxes and labels around them, and saves the annotated image locally as `detected_objects.jpg`.
* **Libraries Used**: `transformers`, `Pillow`, `requests`, `torch`
* **Pip Installation**:
  ```bash
  pip install transformers Pillow requests torch
  ```
* **Models Used**: `facebook/detr-resnet-50` (DEtection TRansformer)
* **How to Run**:
  ```bash
  python any_to_any/img_to_box.py
  ```
* **Expected Output**:
  * A text log listing all detected objects with confidence scores > 0.9 and their exact bounding box pixel coordinates.
  * Saves a newly created file named `detected_objects.jpg` featuring colored bounding boxes and labels.

---

### 11. Image Classification (`any_to_any/img_to_lab.py`)
* **Brief Intro**: Standard visual recognition pipeline that classifies an input image into the top 5 ImageNet classes with accurate confidence percentages.
* **Libraries Used**: `transformers`, `Pillow`, `requests`, `torch`
* **Pip Installation**:
  ```bash
  pip install transformers Pillow requests torch
  ```
* **Models Used**: `google/vit-base-patch16-224` (Vision Transformer - ViT)
* **How to Run**:
  ```bash
  python any_to_any/img_to_lab.py
  ```
* **Expected Output**:
  * Text output displaying top-5 predictions with percentages.
    ```
    Top predictions:
      tabby, tabby cat               56.3%
      tiger cat                      28.1%
      Egyptian cat                   12.8%
      ...
    ```

---

### 12. Text-to-Speech synthesis (`any_to_any/text_to_audio.py`)
* **Brief Intro**: Converts written text into a realistic natural spoken voice file (`.wav`). It utilizes a speaker voice characteristics embedding to model human intonation.
* **Libraries Used**: `torch`, `soundfile`, `transformers`, `datasets`
* **Pip Installation**:
  ```bash
  pip install torch soundfile transformers datasets
  ```
* **Models Used**: `microsoft/speecht5_tts` (SpeechT5) + `microsoft/speecht5-hifigan` (HiFi-GAN vocoder)
* **How to Run**:
  ```bash
  python any_to_any/text_to_audio.py
  ```
* **Expected Output**:
  * Saves a high-quality `.wav` audio file named `output_speech.wav` locally in the active folder.
  * Prints a confirmation with the text that was converted to speech.

---

## ⚠️ Troubleshooting & Notes

* **Large Models and Memory**: Models like `LLaVA-NeXT` (`video_text_to_text.py`) and `ColPali` (`visual_doc_retreival.py`) are heavy. Ensure your computer has sufficient RAM/VRAM. For systems without a GPU, some scripts will fallback to CPU automatically but will run significantly slower.
* **Local Images in Demos**: In `image_text_to_video.py`, please ensure you rename or copy `image-text-to-video-input.jpg` to `image-text-to-video-input.png` or edit the script code to match the `.jpg` extension.
