import requests

# Paste your actual API key here
API_KEY = "qQFcWjcSzn8Uryvgl9yys1vdbYqVVn8Fdupy84cG"

def search_food_usda(query, max_results=1):
    """Search food and return first result's nutrients."""
    url = "https://api.nal.usda.gov/fdc/v1/foods/search"
    params = {
        "api_key": API_KEY,
        "query": query,
        "pageSize": max_results
    }

    response = requests.get(url, params=params)
    data = response.json()

    if 'foods' not in data or len(data['foods']) == 0:
        return {"error": "No food found for query."}

    return extract_nutrition(data['foods'][0])

def extract_nutrition(food_data):
    """Extract calories, protein, carbs, fat from food data."""
    nutrients = {
        "calories": None,
        "protein": None,
        "carbohydrates": None,
        "fat": None
    }

    for nutrient in food_data.get("foodNutrients", []):
        name = nutrient.get("nutrientName", "").lower()
        value = nutrient.get("value")
        unit = nutrient.get("unitName", "g")

        if "energy" in name and "kcal" in unit.lower():
            nutrients["calories"] = f"{value} kcal"
        elif "protein" in name:
            nutrients["protein"] = f"{value} {unit}"
        elif "carbohydrate" in name:
            nutrients["carbohydrates"] = f"{value} {unit}"
        elif "fat" in name:
            nutrients["fat"] = f"{value} {unit}"

    return nutrients
