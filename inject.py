import json
import re

with open("base64_data.json", "r") as f:
    images = json.load(f)

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace image URLs
content = content.replace('"images/berry_oatmeal.png"', f'"{images.get("berry_oatmeal.png", "")}"')
content = content.replace('"images/grilled_chicken.png"', f'"{images.get("grilled_chicken.png", "")}"')
content = content.replace('"images/blueberry_smoothie.png"', f'"{images.get("blueberry_smoothie.png", "")}"')
content = content.replace('"images/avocado_toast.png"', f'"{images.get("avocado_toast.png", "")}"')
content = content.replace('"images/baked_salmon.png"', f'"{images.get("baked_salmon.png", "")}"')

# Also let's fix some CSS details to make the UI ultra-premium and exact.
content = content.replace('--bg-dark: #050505;', '--bg-dark: #0A0A0E;')
content = content.replace('var(--card-bg)', '#1C1C1E') # Apple-like dark mode card
content = content.replace('radial-gradient(var(--border) 1px, transparent 1px)', 'radial-gradient(rgba(255,255,255,0.05) 1px, transparent 1px)')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated index.html with base64 images and tighter CSS.")
