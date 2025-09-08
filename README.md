# 🥗 Food Image Nutrition Tracker

This is an **AI-powered Streamlit application** that estimates the **nutritional values of food items from images**, including **calories, protein, carbohydrates, and fat**. The app uses an **image classification model** to recognize the food, then fetches its nutrition data from the **USDA (United States Department of Agriculture) FoodData Central API**.

---

## 🔍 Key Features

- Detects food items from uploaded images (Indian dishes, fruits, vegetables)
- Predicts **calories, protein, carbs, and fat** per 100g using USDA data
- Generates **bar and pie charts** to visualize nutrient breakdown
- Compares daily intake with **Recommended Dietary Allowance (RDA)**
- Provides **smart dietary suggestions** based on your meal
- Optionally allows you to ask **Gemini AI** questions about the food's health benefits

---

## 🛠 Technologies Used

- **Frontend:** Streamlit  
- **Image Processing:** Pillow, OpenCV  
- **Model:** CNN (TensorFlow/Keras)  
- **Nutrition Data:** USDA API  
- **Data Visualization:** Matplotlib, Pandas  
- **Optional AI Assistant:** Gemini API  

---

## 📁 Project Workflow

1. User uploads a **food image**
2. The app uses a **CNN model** to classify the food
3. Based on the prediction, it queries **USDA API** to fetch nutrients per 100g
4. User enters the **quantity consumed**
5. The app multiplies the values accordingly and displays:
   - Total **calories, protein, carbs, and fats**
   - Pie & bar chart for visual representation
   - Comparison with **RDA**
6. Gemini AI (optional) can answer questions like:  
   > _"Is paneer healthy?"_, _"How much protein is in a banana?"_

---

## 🔧 Setup & Installation

```bash
# Clone the repository
git clone https://github.com/YourUsername/food-nutrition-tracker.git
cd food-nutrition-tracker

# (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
# or
source venv/bin/activate   # On Linux/Mac

# Install dependencies
pip install -r requirements.txt



🔑 API Keys
Create a .env file in the root directory:

ini
Copy
Edit
USDA_API_KEY=your_usda_api_key
GEMINI_API_KEY=your_gemini_api_key  # (Optional)
▶️ Run the App
bash
Copy
Edit
streamlit run app.py
📂 Folder Structure
bash
Copy
Edit
📦 food-nutrition-tracker
├── app.py                  # Streamlit frontend
├── predict_image.py        # Image classification logic
├── usda_api.py             # Fetches nutrition info
├── gemini_ai.py            # Optional AI assistant
├── assets/                 # Backgrounds, logos
├── saved_model/
│   ├── Image_Classify.keras
│   └── class_indices.json
├── requirements.txt
└── README.md
🧪 Sample Use Case
Upload an image of "Paneer"

Model predicts: Paneer

USDA API returns (per 100g):

Calories: 321 kcal

Protein: 25g

Carbs: 3.5g

Fat: 25g

You enter quantity: 200g

Final Output:

Calories: 642 kcal

Protein: 50g

Fat: 50g

Carbs: 7g

🧁 Visualized with pie and bar chart + RDA comparison

👤 Author
Himanshu Gupta
📧 2022blaiml03@axiscoleges.in
🔗 GitHub: Himansh9532
🔗 LinkedIn: Himanshu Gupta

📜 License
This project is licensed under the MIT License.
You are free to use, modify, and share it with proper credit.

🌱 Future Scope
Add voice-based food logging

Expand to full meal tracking + fitness integration

Integrate OCR to read nutrition from food labels

Add support for Indian nutritional databases

yaml
Copy
Edit

---

✅ You can copy-paste this as your `README.md` file in your project folder.  
Let me know if you want to:
- Add a GIF/image preview
- Generate the file for download
- Customize the project name/logo/URL
