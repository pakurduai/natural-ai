from PIL import Image, ImageChops

def extract_thumbnails(image_path, prefix, expected_w=100, expected_h=100):
    img = Image.open(image_path).convert('RGB')
    w, h = img.size
    
    # We will look for rectangles that are significantly different from the background
    # Background is roughly (10, 10, 10) or (20, 20, 20)
    bg_color = (15, 15, 15)
    
    # A simple way to find images is to look at a vertical line on the left side (x ~ 10% to 20% of width)
    # where the meal thumbnails usually are.
    x_scan = int(w * 0.15)
    
    thumbnails = []
    in_image = False
    start_y = 0
    
    # Scan down the left side
    for y in range(h):
        r, g, b = img.getpixel((x_scan, y))
        is_colorful = (r > 40 or g > 40 or b > 40)
        
        if is_colorful and not in_image:
            in_image = True
            start_y = y
        elif not is_colorful and in_image:
            in_image = False
            end_y = y
            height = end_y - start_y
            if 50 < height < int(h * 0.3): # Reasonable thumbnail height
                # We found the vertical bounds. Now find horizontal bounds.
                # Scan horizontally from x_scan left and right
                left_x = x_scan
                while left_x > 0:
                    r2,g2,b2 = img.getpixel((left_x, start_y + height//2))
                    if r2 < 30 and g2 < 30 and b2 < 30:
                        break
                    left_x -= 1
                    
                right_x = x_scan
                while right_x < w - 1:
                    r2,g2,b2 = img.getpixel((right_x, start_y + height//2))
                    if r2 < 30 and g2 < 30 and b2 < 30:
                        break
                    right_x += 1
                
                width = right_x - left_x
                if 50 < width < int(w * 0.5):
                    thumbnails.append((left_x, start_y, right_x, end_y))

    print(f"Found {len(thumbnails)} thumbnails in {image_path}")
    for i, box in enumerate(thumbnails):
        crop = img.crop(box)
        crop.save(f"images/{prefix}_{i}.png")
        print(f"Saved images/{prefix}_{i}.png -> {box}")

extract_thumbnails('meal history.png', 'meal')
extract_thumbnails('dashboard.png', 'dash')
