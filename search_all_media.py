import os
import glob
from PIL import Image

art_dir = "C:/Users/waseem/.gemini/antigravity-ide/brain/dd20693a-b329-4f05-91be-0131cde6c3b4"
files = glob.glob(os.path.join(art_dir, "media__*.png"))

for path in files:
    img = Image.open(path).convert("RGB")
    w, h = img.size
    red_count = 0
    for y in range(0, h, 2): # scan every 2nd row for speed
        for x in range(0, w, 2):
            r, g, b = img.getpixel((x, y))
            # Saturated red annotation
            if r > 200 and g < 50 and b < 50:
                red_count += 1
                
    if red_count > 100:
        print(f"File {os.path.basename(path)} has {red_count} red pixels!")
