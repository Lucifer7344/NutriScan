from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

# Load CLIP model and processor
model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Extended food label list (editable)
food_labels = [
    # Fruits
    "apple", "banana", "grapes", "orange", "mango", "watermelon", "pineapple", "papaya", "kiwi", "pear",
    "peach", "plum", "cherry", "strawberry", "blueberry", "raspberry", "blackberry", "pomegranate", "coconut",
    "lychee", "apricot", "fig", "date", "melon", "guava", "passion fruit", "dragon fruit", "jackfruit",
    "tamarind", "jamun", "custard apple",

    # Vegetables
    "carrot", "tomato", "potato", "cucumber", "onion", "garlic", "spinach", "lettuce", "broccoli", "cauliflower",
    "cabbage", "bell pepper", "chili pepper", "zucchini", "eggplant", "pumpkin", "sweet potato", "radish",
    "beetroot", "okra", "corn", "peas", "green beans", "asparagus", "mushroom", "leek", "celery",

    # Legumes & grains
    "rice", "brown rice", "quinoa", "barley", "oats", "wheat", "lentils", "chickpeas", "black beans",
    "kidney beans", "soybeans", "moong dal", "urad dal",

    # Common dishes
    "pizza", "burger", "pasta", "fried rice", "sushi", "steak", "salad", "chicken curry", "paneer tikka",
    "biryani", "dal tadka", "masala dosa", "idli", "samosa", "naan", "tandoori chicken", "fish curry",
    "chole", "palak paneer", "pav bhaji", "rajma chawal", "veg pulao", "aloo paratha", "kadhi", "khichdi",
    "spring rolls", "momos", "hakka noodles", "veg manchurian", "chilli paneer", "chilli chicken",
    "cheese sandwich", "paneer sandwich", "peanut butter", "peanut butter sandwich", "peanut butter paneer",
    "butter paneer", "shahi paneer", "grilled paneer", "stuffed paratha", "kathi roll", "veg wrap",
    "chicken biryani", "mutton curry", "egg curry", "egg fried rice", "omelette", "egg roll",

    # Desserts
    "ice cream", "cake", "cheesecake", "brownie", "cupcake", "donut", "pudding", "muffin", "tiramisu",
    "gulab jamun", "jalebi", "rasgulla", "barfi", "laddu", "kheer", "halwa", "apple pie", "milk cake",
    "chocolate", "cookies", "chocolate bar", "kulfi", "falooda", "payasam", "basundi",

    # Beverages
    "coffee", "tea", "green tea", "black coffee", "milk", "buttermilk", "smoothie", "lassi", "fruit juice",
    "orange juice", "apple juice", "lemonade", "cold drink", "coca cola", "sprite", "pepsi", "fanta",
    "energy drink", "red bull", "mojito", "milkshake", "banana shake", "mango shake", "badam milk",

    # More dishes
    "noodles", "ramen", "udon", "pho", "miso soup", "tom yum soup", "chicken nuggets", "french fries",
    "mac and cheese", "caesar salad", "coleslaw", "bbq ribs", "pancakes", "waffles", "hot dog", "tacos",
    "burrito", "nachos", "hummus", "falafel", "shwarma", "gyros", "fish and chips", "grilled cheese",
    "stuffed peppers", "lasagna", "spaghetti", "chow mein", "fried chicken", "shrimp tempura", "grilled fish"
]

def predict_top_k(image_path, candidate_labels=food_labels, top_k=3):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(text=candidate_labels, images=image, return_tensors="pt", padding=True).to(device)

    with torch.no_grad():
        outputs = model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)

    top_probs, top_idxs = probs.topk(top_k)
    results = [(candidate_labels[i], round(p.item(), 4)) for i, p in zip(top_idxs[0], top_probs[0])]
    return results
