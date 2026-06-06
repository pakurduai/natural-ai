import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

new_foods = '''    const DEFAULT_FOODS = [
      { id: 1, name: "Berry Oatmeal", kcal: 400, p: 18, c: 54, f: 15, img: "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?w=200" },
      { id: 2, name: "Grilled Chicken Bowl", kcal: 560, p: 38, c: 62, f: 16, img: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=200" },
      { id: 3, name: "Blueberry Smoothie", kcal: 230, p: 10, c: 32, f: 6, img: "https://images.unsplash.com/photo-1553530666-ba11a7da3888?w=200" },
      { id: 4, name: "Avocado Toast", kcal: 310, p: 9, c: 30, f: 17, img: "https://images.unsplash.com/photo-1588137378633-dea1336ce1e2?w=200" },
      { id: 5, name: "Baked Salmon", kcal: 380, p: 42, c: 8, f: 22, img: "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=200" },
      { id: 6, name: "Caesar Salad", kcal: 290, p: 14, c: 18, f: 19, img: "https://images.unsplash.com/photo-1512852939750-1305098529bf?w=200" },
      { id: 7, name: "Banana Pancakes", kcal: 340, p: 12, c: 52, f: 10, img: "https://images.unsplash.com/photo-1528207776546-365bb710ee93?w=200" },
      { id: 8, name: "Greek Yogurt Bowl", kcal: 220, p: 20, c: 28, f: 4, img: "https://images.unsplash.com/photo-1488477181228-c84b34b8e007?w=200" },
      { id: 9, name: "Quinoa Power Bowl", kcal: 420, p: 16, c: 58, f: 14, img: "https://images.unsplash.com/photo-1546793665-c74683f339c1?w=200" },
      { id: 10, name: "Veggie Stir Fry", kcal: 280, p: 11, c: 38, f: 9, img: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=200" }
    ];'''

# We need to replace the existing DEFAULT_FOODS array which might have huge base64 strings.
# The pattern should match from "const DEFAULT_FOODS = [" to the closing "];"
pattern = re.compile(r'const DEFAULT_FOODS\s*=\s*\[.*?\];', re.DOTALL)
new_content = pattern.sub(new_foods, content)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Replaced DEFAULT_FOODS with Unsplash URLs.")
