from diffusers import StableVideoDiffusionPipeline
from PIL import Image
import torch

# Load model
pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid-xt",
    torch_dtype=torch.float16
)

pipe.to("cpu")

# Load image
image = Image.open("image-text-to-video-input.jpg").convert("RGB")

# Generate frames
frames = pipe(
    image,
    decode_chunk_size=8
).frames[0]

print("Video Frames Generated")