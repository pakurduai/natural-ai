import cv2
import numpy as np

img = cv2.imread('meal history.png')
if img is None:
    exit()

# Convert to HSV to find colorful regions (food images)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# Threshold saturation to find non-gray regions
_, s_thresh = cv2.threshold(hsv[:,:,1], 40, 255, cv2.THRESH_BINARY)

# Find contours of the colorful regions
contours, _ = cv2.findContours(s_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

boxes = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    aspect_ratio = float(w)/h
    if 0.5 < aspect_ratio < 1.5 and 40 < w < 200:
        boxes.append((y, x, w, h))

boxes.sort()

# Merge overlapping/close boxes
merged = []
for b in boxes:
    if not merged:
        merged.append(b)
    else:
        last_b = merged[-1]
        # if distance is less than 50 pixels, maybe it's the same image
        if abs(b[0] - last_b[0]) < 50:
            # merge them
            min_y = min(b[0], last_b[0])
            min_x = min(b[1], last_b[1])
            max_y = max(b[0]+b[3], last_b[0]+last_b[3])
            max_x = max(b[1]+b[2], last_b[1]+last_b[2])
            merged[-1] = (min_y, min_x, max_x-min_x, max_y-min_y)
        else:
            merged.append(b)

names = ["oatmeal", "chicken", "smoothie", "toast", "salmon"]

print(f"Found {len(merged)} potential image boxes.")
for i, (y, x, w, h) in enumerate(merged):
    if i < len(names):
        # Crop slightly larger to ensure we get the full image
        pad = 5
        y1 = max(0, y-pad)
        y2 = min(img.shape[0], y+h+pad)
        x1 = max(0, x-pad)
        x2 = min(img.shape[1], x+w+pad)
        crop = img[y1:y2, x1:x2]
        
        # force resize to 200x200
        crop = cv2.resize(crop, (200, 200))
        cv2.imwrite(f"{names[i]}.png", crop)
        print(f"Saved {names[i]}.png")
