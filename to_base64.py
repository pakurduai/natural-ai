import base64
import json
import os

images_dir = "images"
files = ["berry_oatmeal.png", "grilled_chicken.png", "blueberry_smoothie.png", "avocado_toast.png", "baked_salmon.png"]

base64_images = {}

for f in files:
    path = os.path.join(images_dir, f)
    if os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
            base64_images[f] = f"data:image/png;base64,{encoded}"

with open("base64_data.json", "w") as out:
    json.dump(base64_images, out)
print("Base64 conversion complete.")
