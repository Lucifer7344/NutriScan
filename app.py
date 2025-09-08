import streamlit as st
import os
import base64
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

from predict_image import predict_top_k
from usda_api import search_food_usda
from gemini_ai import ask_gemini  # Optional

# -------------- SET BACKGROUND IMAGE & STYLING --------------
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    css = f"""
    <style>
    #MainMenu, header, footer {{ visibility: hidden; }}
    section[data-testid="stHeader"] {{ display: none; }}

    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        font-family: 'Nunito', sans-serif;
        color: white;
    }}

    .main-container {{
        background-color: rgba(255, 255, 255, 0.06);
        padding: 2rem;
        border-radius: 20px;
        max-width: 900px;
        margin: auto;
        box-shadow: 0 0 30px rgba(0,0,0,0.4);
    }}

    h1, h2, h3, h4 {{
        font-weight: 700;
        color: #ffffff;
    }}

    .stTextInput input, .stNumberInput input {{
        background-color: #1e1e1e;
        color: white;
        border-radius: 8px;
        border: none;
    }}

    .stFileUploader {{
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 0.5rem;
    }}

    .stButton > button {{
        background-color: #ff5c5c;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: bold;
    }}

    .stButton > button:hover {{
        background-color: #ff7777;
        color: white;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("flat-lay-sport-frame-with-salad_23-2148531521.avif")

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if "meal_log" not in st.session_state:
    st.session_state.meal_log = []
if "predicted_food" not in st.session_state:
    st.session_state.predicted_food = None
    st.session_state.food_image_path = None
    st.session_state.food_quantity = 100.0
if "trigger_prediction" not in st.session_state:
    st.session_state.trigger_prediction = False

st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.title("Daily Calorie & Nutrition Tracker")

tab1, tab2 = st.tabs(["Add Food", "Ask AI"])

with tab1:
    st.subheader("Add Food to Meal Log")

    uploaded_file = st.file_uploader("Upload food image", type=["jpg", "jpeg", "png"])
    manual_name = st.text_input("Or enter food name manually")
    quantity = st.number_input("Quantity (in grams)", min_value=1.0, value=100.0)

    if uploaded_file and not st.session_state.predicted_food:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        results = predict_top_k(file_path)
        st.session_state.predicted_food = results[0][0]
        st.session_state.food_image_path = file_path
        st.session_state.food_quantity = quantity
        st.session_state.trigger_prediction = True

    elif manual_name.strip() and not st.session_state.predicted_food:
        st.session_state.predicted_food = manual_name.strip()
        st.session_state.food_quantity = quantity
        st.session_state.trigger_prediction = True

    if st.session_state.trigger_prediction and st.session_state.predicted_food:
        st.success(f"Food Name: {st.session_state.predicted_food.title()} — Please confirm to add.")
        st.session_state.trigger_prediction = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Confirm and Add"):
            if st.session_state.predicted_food:
                result = search_food_usda(st.session_state.predicted_food)
                if "error" in result:
                    st.error(result["error"])
                else:
                    entry = {
                        "Food": st.session_state.predicted_food.title(),
                        "Quantity (g)": st.session_state.food_quantity
                    }
                    for k in ["calories", "protein", "carbohydrates", "fat"]:
                        try:
                            val = float(result[k].split()[0])
                            entry[k.capitalize()] = round(val * st.session_state.food_quantity / 100, 2)
                        except:
                            entry[k.capitalize()] = 0.0
                    st.session_state.meal_log.append(entry)
                    st.success(f"{st.session_state.predicted_food.title()} added!")
                    st.session_state.predicted_food = None
                    st.session_state.food_image_path = None
    with col2:
        if st.button("Clear Meal Log"):
            st.session_state.meal_log = []
            st.session_state.predicted_food = None
            st.session_state.food_image_path = None
            st.info("Meal log cleared.")

    if st.session_state.meal_log:
        st.subheader("Meal Log")
        for idx, entry in enumerate(st.session_state.meal_log):
            cols = st.columns([6, 1])
            with cols[0]:
                st.markdown(
                    f"**{idx+1}. {entry['Food']}** — {entry['Quantity (g)']}g | "
                    f"Calories: {entry.get('Calories', 0)} | Protein: {entry.get('Protein', 0)}g | "
                    f"Carbs: {entry.get('Carbohydrates', 0)}g | Fat: {entry.get('Fat', 0)}g"
                )
            with cols[1]:
                if st.button("Delete", key=f"delete_{idx}"):
                    st.session_state.meal_log.pop(idx)
                    st.rerun()

        df = pd.DataFrame(st.session_state.meal_log)
        rda = {"Calories": 2000, "Protein": 50, "Carbohydrates": 300, "Fat": 70}
        total = {k: round(df[k].sum(), 2) for k in rda.keys()}

        st.subheader("Nutrient Breakdown (Pie Chart)")
        fig1, ax1 = plt.subplots(facecolor='none')
        ax1.pie(total.values(), labels=total.keys(), autopct='%1.1f%%', startangle=90,
                colors=["#2980b9", "#27ae60", "#e67e22", "#c0392b"])
        ax1.axis("equal")
        fig1.patch.set_alpha(0)
        st.pyplot(fig1)

        st.subheader("Nutrient Intake (Bar Chart)")
        fig2, ax2 = plt.subplots(facecolor='none')
        ax2.set_facecolor('none')
        bars = ax2.bar(total.keys(), total.values(), color=["#2980b9", "#27ae60", "#e67e22", "#c0392b"], edgecolor='white')
        ax2.set_ylabel("Total Intake", color='white')
        ax2.set_title("Nutrient Intake", color='white', fontsize=14)
        ax2.tick_params(colors='white')
        for i, value in enumerate(total.values()):
            ax2.text(i, value + 5, str(value), ha='center', va='bottom', color='white', fontweight='bold')
        fig2.patch.set_alpha(0)
        st.pyplot(fig2)

        st.subheader("RDA Comparison")
        rda_df = pd.DataFrame({"Consumed": total, "Recommended (RDA)": rda})
        st.dataframe(rda_df.T)

        st.subheader("Daily Intake Suggestion")
        for nutrient in rda:
            if total[nutrient] < rda[nutrient]:
                diff = rda[nutrient] - total[nutrient]
                st.info(f"You're {diff} {nutrient.lower()} short of your daily goal. Consider adding more {nutrient.lower()}-rich foods.")
            else:
                st.success(f"You have met or exceeded your daily {nutrient.lower()} intake.")

with tab2:
    st.subheader("Ask AI About Your Nutrition")
    query = st.text_input("Ask any nutrition-related question:")
    if st.button("Ask AI"):
        if query.strip():
            response = ask_gemini(query)
            st.markdown(f"**AI Response:**\n{response}")
        else:
            st.warning("Please enter a valid question.")

st.markdown("</div>", unsafe_allow_html=True)
