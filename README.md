## NutriScan 

An **AI-powered Streamlit application** that estimates the nutritional values of food items from images, including **calories, protein, carbohydrates, and fat**.  

The app uses a **CNN model** to recognize food images, then fetches its nutrition data from the **USDA FoodData Central API**.  
Optionally, it integrates **Gemini AI** to answer health-related questions about food.  

---

## 🔍 Key Features
- 📸 Detects food items from uploaded images (supports Indian dishes, fruits, and vegetables).  
- 🔢 Predicts **calories, protein, carbs, and fat per 100g** using USDA data.  
- 📊 Generates **bar and pie charts** to visualize nutrient breakdown.  
- ✅ Compares daily intake with **Recommended Dietary Allowance (RDA)**.  
- 💡 Provides **smart dietary suggestions** based on your meal.  
- 🤖 (Optional) Ask **Gemini AI** questions like *“Is paneer healthy?”* or *“How much protein is in a banana?”*.  

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
1. User uploads a **food image**.  
2. The app’s **CNN model** classifies the food.  
3. Based on the prediction, it queries **USDA API** to fetch nutrients per 100g.  
4. User enters the **quantity consumed**.  
5. App calculates and displays:  
   - ✅ Total calories, protein, carbs, fats  
   - 📊 Pie & bar chart for visualization  
   - ⚖️ Comparison with RDA  
6. (Optional) **Gemini AI** answers your health-related queries.  

---

## 🔧 Setup & Installation


1. Clone the repository
   ```bash
   git clone https://github.com/Lucifer7344/NutriScan.git
   cd NutriScan

2. Create a virtual environment
   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   source venv/bin/activate  # On Linux/Mac

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   
4. 🔑 API Keys
   Create a .env file in the root directory with:
   ```bash
   USDA_API_KEY=your_usda_api_key
   GEMINI_API_KEY=your_gemini_api_key  # (Optional)
   
5. ▶️ Run the App
   ```bash
   streamlit run app.py
6. 📂 Folder Structure
   ```bash
   📦 NutriScan
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
7. 🧪 Sample Use Case

   Upload an image of Paneer

   1. Model predicts: Paneer

   2. USDA API returns (per 100g):

   3. Calories: 321 kcal

   4. Protein: 25g

   5. Carbs: 3.5g

   6. Fat: 25g

   You enter 200g → Final Output:

   1. Calories: 642 kcal

   2. Protein: 50g

   3. Carbs: 7g

   4. Fat: 50g

   ✅ Visualized with pie and bar chart + RDA comparison

🌱 Future Scope

🎙 Add voice-based food logging

📅 Expand to full meal tracking + fitness integration

🏷 Integrate OCR to read nutrition from food labels

🍲 Add support for Indian nutritional databases
