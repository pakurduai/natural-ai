from PIL import Image
import os

path = "C:/Users/waseem/.gemini/antigravity-ide/brain/dd20693a-b329-4f05-91be-0131cde6c3b4/media__1780799374528.png"
if os.path.exists(path):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    
    # We will find contiguous clusters of red pixels using standard BFS/DFS
    visited = set()
    clusters = []
    
    red_pts = set()
    for y in range(h):
        for x in range(w):
            r, g, b = img.getpixel((x, y))
            if r > 200 and g < 100 and b < 100:
                red_pts.add((x, y))
                
    for pt in red_pts:
        if pt in visited:
            continue
        # BFS to find cluster
        cluster = []
        queue = [pt]
        visited.add(pt)
        while queue:
            curr = queue.pop(0)
            cluster.append(curr)
            # Check neighbors
            cx, cy = curr
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = cx + dx, cy + dy
                    if (nx, ny) in red_pts and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        # Keep clusters with a reasonable size
        if len(cluster) > 10:
            xs = [p[0] for p in cluster]
            ys = [p[1] for p in cluster]
            clusters.append((min(xs), min(ys), max(xs), max(ys), len(cluster)))
            
    print(f"Found {len(clusters)} red clusters:")
    for i, (min_x, min_y, max_x, max_y, size) in enumerate(clusters):
        print(f"  Cluster {i+1}: box=({min_x}, {min_y}) to ({max_x}, {max_y}), size={size} px")
        # Save each crop to help inspect
        crop_box = (max(0, min_x - 10), max(0, min_y - 10), min(w, max_x + 10), min(h, max_y + 10))
        img.crop(crop_box).save(f"C:/Users/waseem/.gemini/antigravity-ide/brain/dd20693a-b329-4f05-91be-0131cde6c3b4/red_cluster_{i+1}.png")
        print(f"    Saved crop to red_cluster_{i+1}.png")
else:
    print("Screenshot doesn't exist")
