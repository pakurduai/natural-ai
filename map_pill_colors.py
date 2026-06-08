from PIL import Image

img = Image.open("C:/Users/waseem/.gemini/antigravity-ide/brain/dd20693a-b329-4f05-91be-0131cde6c3b4/mockup_pill.png")
w, h = img.size

# We will scan the image and find rows where there are text/colored pixels.
# Let's print out the character representation for each row in detail.
# Let's map:
# Black background (10, 15, 44) -> ' '
# Card bg (26, 26, 26) -> '.'
# Lime green (212, 255, 0) -> 'Y'
# Bright green (57, 255, 20) -> 'G'
# White (255, 255, 255) -> 'W'
# Others -> '?'

output = []
for y in range(h):
    row = []
    has_content = False
    for x in range(w):
        r, g, b = img.getpixel((x, y))
        
        # Check colors
        if r == 10 and g == 15 and b == 44:
            c = ' '
        elif r == 26 and g == 26 and b == 26:
            c = '.'
        elif r > 180 and g > 220 and b < 50:
            c = 'Y'
            has_content = True
        elif r < 100 and g > 200 and b < 100:
            c = 'G'
            has_content = True
        elif r > 200 and g > 200 and b > 200:
            c = 'W'
            has_content = True
        else:
            # Check proximity to known colors
            dist_bg = (r-10)**2 + (g-15)**2 + (b-44)**2
            dist_pill = (r-26)**2 + (g-26)**2 + (b-26)**2
            dist_yellow = (r-212)**2 + (g-255)**2 + (b-0)**2
            dist_green = (r-57)**2 + (g-255)**2 + (b-20)**2
            dist_white = (r-255)**2 + (g-255)**2 + (b-255)**2
            
            m = min(dist_bg, dist_pill, dist_yellow, dist_green, dist_white)
            if m == dist_bg:
                c = ' '
            elif m == dist_pill:
                c = '.'
            elif m == dist_yellow:
                c = 'Y'
                has_content = True
            elif m == dist_green:
                c = 'G'
                has_content = True
            else:
                c = 'W'
                has_content = True
        row.append(c)
    if has_content:
        output.append((y, "".join(row)))

print(f"Content rows in mockup pill: {len(output)}")
with open("C:/Users/waseem/.gemini/antigravity-ide/brain/dd20693a-b329-4f05-91be-0131cde6c3b4/pill_detailed_map.txt", "w") as f:
    for y, row in output:
        # Save only the horizontal window where the content is (between first and last non-space)
        first = len(row) - len(row.lstrip())
        last = len(row.rstrip())
        f.write(f"Row {y:03d}: " + row[first:last] + "\n")
