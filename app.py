import streamlit as st
from recommendation_engine import recommend_recipes
import warnings
warnings.filterwarnings("ignore")


# ------------------ Page Config ------------------ #
st.set_page_config(
    page_title="Chill Chef – Recipe Recommender",
    page_icon="🍽️",
    layout="wide"
)

# ------------------ Custom CSS ------------------ #
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #fff7e6, #ffffff);
        font-family: 'Segoe UI', sans-serif;
    }
    .header-title {
        color: #d35400;
        font-size: 42px;
        text-align: center;
        font-weight: bold;
    }
    .sub-header {
        color: #5d4037;
        text-align: center;
        margin-bottom: 30px;
        font-size: 20px;
    }
    .recipe-card {
        background-color: #fff9f0;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.1);
        margin: 10px;
    }
    .recipe-title {
        color: #e67e22;
        font-size: 20px;
        font-weight: bold;
        margin-top: 10px;
    }
    .recipe-meta {
        color: #616161;
        font-size: 16px;
        margin-bottom: 10px;
    }
    .recipe-link-button {
        background-color: #ff914d;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        margin-top: 10px;
    }
    .recipe-link-button:hover {
        background-color: #ffae6b;
    }
    .stButton>button {
        background-color: #ff914d;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
        font-size: 16px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ffa366;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ Header ------------------ #
st.markdown("<div class='header-title'>🥕 Chill Chef – Recipe Recommender 🍅</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Type in the ingredients you have, and we’ll find delicious recipes for you!</div>", unsafe_allow_html=True)

# ------------------ Input ------------------ #
user_input = st.text_input("Enter available ingredients (comma-separated)", placeholder="e.g., tomato, onion, garlic, egg")

if st.button("🍳 Recommend Recipes"):
    if user_input.strip() == "":
        st.warning("Please enter some ingredients to get recommendations.")
    else:
        recommendations = recommend_recipes(user_input)
        
        st.markdown("<h3 style='color: black; font-weight: bold;'>🥗 Top Recipe Picks</h3>", unsafe_allow_html=True)

        cols = st.columns(3)
        
        for i, recipe in enumerate(recommendations):
            with cols[i % 3]:
                st.markdown("<div class='recipe-card'>", unsafe_allow_html=True)
                st.image(recipe['image'], use_container_width=True)
                st.markdown(f"<div class='recipe-title'>{recipe['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='recipe-meta'>🕒 {recipe['time']} | 📈 Difficulty: {recipe['Difficulty']}</div>", unsafe_allow_html=True)
                st.markdown(f"<a class='recipe-link-button' href='{recipe['url']}' target='_blank'>View Recipe</a>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
