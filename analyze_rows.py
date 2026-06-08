from PIL import Image

img = Image.open("dashboard.png")
w, h = img.size

# Let's search the top part (y = 150 to 600) for white or bright pixels (text) and list their vertical positions
text_rows = []
for y in range(150, 600):
    bright_pixels = 0
    green_pixels = 0
    for x in range(w):
        r, g, b = img.getpixel((x, y))
        # Text is usually white or light gray (R > 180, G > 180, B > 180)
        if r > 180 and g > 180 and b > 180:
            bright_pixels += 1
        # Ring is green (G > 180, R < 100, B < 100)
        if g > 180 and r < 100 and b < 100:
            green_pixels += 1
            
    if bright_pixels > 5 or green_pixels > 5:
        text_rows.append((y, bright_pixels, green_pixels))

# Group them into clusters to find where labels are
print("Row analysis (y, bright/text, green/ring):")
for r in text_rows[::5]:
    print(f"  Row {r[0]}: Text px: {r[1]}, Green px: {r[2]}")
