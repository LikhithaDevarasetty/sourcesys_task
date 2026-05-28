# Task 5: Text to Speech (Text → Audio)
# Model: microsoft/speecht5_tts

import torch
import soundfile as sf
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset

print("Loading TTS models...")
processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5-hifigan")

# Load a speaker embedding (voice characteristics)
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

# Text to convert to speech
text = "Hello! This is a text to speech demo using Hugging Face transformers."

inputs = processor(text=text, return_tensors="pt")

with torch.no_grad():
    speech = model.generate_speech(
        inputs["input_ids"],
        speaker_embeddings,
        vocoder=vocoder
    )

# Save the audio file
output_file = "output_speech.wav"
sf.write(output_file, speech.numpy(), samplerate=16000)

print(f"Speech saved to: {output_file}")
print(f"Text spoken: {text}")