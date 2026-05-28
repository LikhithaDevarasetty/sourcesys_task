# Audio + Question → Answer (uses built-in LibriSpeech sample — no audio file needed!)
# Downloads a small sample audio automatically from torchaudio datasets
#
# pip install transformers torch torchaudio soundfile

import torch
import torchaudio
from transformers import (
    Wav2Vec2ForCTC,
    Wav2Vec2Processor,
    AutoTokenizer,
    AutoModelForQuestionAnswering,
)

# ── Step 1: Load speech-to-text model ────────────────────────────────────────

print("Loading speech recognition model...")
stt_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
stt_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
print("Speech model ready.\n")

# ── Step 2: Load QA model ─────────────────────────────────────────────────────

print("Loading QA model...")
qa_tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
qa_model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")
print("QA model ready.\n")

# ── Step 3: Download a sample audio from LibriSpeech dataset ─────────────────

print("Downloading LibriSpeech sample audio (small, ~1MB)...")
dataset = torchaudio.datasets.LIBRISPEECH(".", url="test-clean", download=True)

# Take the first sample
waveform, sample_rate, transcript, speaker_id, chapter_id, utterance_id = dataset[0]

print(f"\nAudio info:")
print(f"  Sample rate : {sample_rate} Hz")
print(f"  Duration    : {waveform.shape[1] / sample_rate:.2f} seconds")
print(f"  Speaker ID  : {speaker_id}")
print(f"  Real transcript (ground truth): {transcript.lower()}\n")

# Resample to 16000 Hz if needed
if sample_rate != 16000:
    waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)

# ── Step 4: Transcribe audio → text ──────────────────────────────────────────

print("=" * 60)
print("STEP 1 — Transcribing audio")
print("=" * 60)

inputs = stt_processor(
    waveform.squeeze().numpy(),
    sampling_rate=16000,
    return_tensors="pt",
).input_values

with torch.no_grad():
    logits = stt_model(inputs).logits

ids = torch.argmax(logits, dim=-1)
context = stt_processor.decode(ids[0]).lower()

print(f"\nTranscription: {context}\n")

# ── Step 5: Answer questions from the transcription ───────────────────────────

def answer_question(context, question):
    inputs = qa_tokenizer(question, context, return_tensors="pt", truncation=True)

    with torch.no_grad():
        outputs = qa_model(**inputs)

    start = torch.argmax(outputs.start_logits)
    end   = torch.argmax(outputs.end_logits) + 1

    answer = qa_tokenizer.convert_tokens_to_string(
        qa_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start:end])
    )
    return answer.strip()


# Ask questions about what was spoken
questions = [
    "What is being talked about?",
    "What action is mentioned?",
    "Who or what is the subject?",
]

print("=" * 60)
print("STEP 2 — Answering questions")
print("=" * 60)

for q in questions:
    ans = answer_question(context, q)
    print(f"\nQ: {q}")
    print(f"A: {ans}")

print("\n" + "=" * 60)
print("Done!")