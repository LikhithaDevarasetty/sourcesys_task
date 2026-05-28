from transformers import AutoProcessor, LlavaNextVideoForConditionalGeneration
import torch, cv2, numpy as np

model_id = "llava-hf/LLaVA-NeXT-Video-7B-hf"
processor = AutoProcessor.from_pretrained(model_id)
model = LlavaNextVideoForConditionalGeneration.from_pretrained(
    model_id, torch_dtype=torch.float16, device_map="auto"
)

def extract_frames(video_path, num_frames=8):
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    indices = np.linspace(0, total - 1, num_frames, dtype=int)
    frames = []
    for i in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cap.release()
    return frames

video_frames = extract_frames("input.mp4", num_frames=8)

conversation = [{
    "role": "user",
    "content": [
        {"type": "video"},
        {"type": "text", "text": "What is happening in this video?"}
    ]
}]

prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
inputs = processor(text=prompt, videos=[video_frames], return_tensors="pt").to("cuda")

output = model.generate(**inputs, max_new_tokens=200)
print(processor.decode(output[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True))