# Remove black background from the provided image and export with transparency

from PIL import Image
import numpy as np

input_path = "Redwatch-Shiel-Tech-A-v0.1.png"
output_path = "redwatch_shield_transparent.png"

img = Image.open(input_path).convert("RGBA")
data = np.array(img)

# Identify near-black pixels (background) and make them transparent
r, g, b, a = data.T
threshold = 20  # tolerance for "black"
black_mask = (r < threshold) & (g < threshold) & (b < threshold)

data[..., 3][black_mask.T] = 0  # set alpha to 0 for background

result = Image.fromarray(data)
result.save(output_path)

output_path
