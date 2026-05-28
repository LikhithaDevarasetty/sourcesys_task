# Speech Recognition — uses LibriSpeech dataset (no audio file needed!)
# pip install transformers torch torchaudio

import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Load model
print("Loading speech recognition model...")
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
print("Model ready.\n")

# Download LibriSpeech test sample (~1MB, downloads automatically)
print("Downloading LibriSpeech sample audio...")
dataset = torchaudio.datasets.LIBRISPEECH(".", url="test-clean", download=True)

# Try multiple samples so you can see different transcriptions
num_samples = 3

print(f"\nTranscribing {num_samples} audio samples from LibriSpeech...\n")
print("=" * 60)

for i in range(num_samples):
    waveform, sample_rate, ground_truth, speaker_id, chapter_id, utterance_id = dataset[i]

    # Resample to 16000 Hz if needed
    if sample_rate != 16000:
        waveform = torchaudio.functional.resample(waveform, sample_rate, 16000)

    # Transcribe
    input_values = processor(
        waveform.squeeze().numpy(),
        sampling_rate=16000,
        return_tensors="pt"
    ).input_values

    with torch.no_grad():
        logits = model(input_values).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])

    duration = waveform.shape[1] / 16000

    print(f"Sample {i + 1}")
    print(f"  Speaker ID      : {speaker_id}")
    print(f"  Duration        : {duration:.2f} seconds")
    print(f"  Ground truth    : {ground_truth.lower()}")
    print(f"  Model output    : {transcription.lower()}")
    print("-" * 60)