import cv2
import numpy as np

# Load the image
img = cv2.imread('meal history.png')
if img is None:
    print("Could not load meal history.png")
    exit()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# The images are probably inside rounded rectangles. Let's find contours.
# Apply edge detection
edges = cv2.Canny(gray, 50, 150)
kernel = np.ones((5,5), np.uint8)
closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

count = 1
extracted = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    # The thumbnails are probably roughly square, maybe 60-120 pixels wide
    aspect_ratio = float(w)/h
    if 0.8 < aspect_ratio < 1.2 and 50 < w < 200:
        extracted.append((y, x, w, h))

# Sort by Y coordinate to get them in order top to bottom
extracted.sort()

# Remove duplicates or overlapping boxes
final_boxes = []
for b in extracted:
    if not final_boxes:
        final_boxes.append(b)
    else:
        # Check if it overlaps heavily with the last one
        last_b = final_boxes[-1]
        if abs(b[0] - last_b[0]) > 20: # Must be at least 20px apart vertically
            final_boxes.append(b)

names = ["oatmeal", "chicken", "smoothie", "toast", "salmon"]

print(f"Found {len(final_boxes)} potential image boxes.")
for i, (y, x, w, h) in enumerate(final_boxes):
    if i < len(names):
        crop = img[y:y+h, x:x+w]
        cv2.imwrite(f"{names[i]}.png", crop)
        print(f"Saved {names[i]}.png")
