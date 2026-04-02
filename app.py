import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import plotly.express as px


# ---------------- CONFIG ----------------
st.set_page_config(page_title="Agri AI System", layout="wide")

# ---------------- USER DATABASE ----------------
USER_FILE = "users.json"

def load_users():
    try:
        with open(USER_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- AUTH SYSTEM ----------------
def login_register():

    st.title("🔐 Welcome to Agri AI System")

    choice = st.radio("Select", ["Login", "Register"])

    users = load_users()

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Register":
        if st.button("Create Account"):
            if username in users:
                st.warning("User already exists")
            else:
                users[username] = password
                save_users(users)
                st.success("Account created! Please login.")

    else:
        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.user = username
                st.success(f"Welcome {username} ✅")
            else:
                st.error("Invalid credentials")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("irrigation_prediction.csv")

# ---------------- LOAD MODELS ----------------
crop_model = None
irrigation_model = None

try:
    crop_model = pickle.load(open("crop_model.pkl", "rb"))
except:
    pass

try:
    irrigation_model = pickle.load(open("irrigation_model.pkl", "rb"))
except:
    pass

# ---------------- MAIN APP ----------------
if not st.session_state.user:
    login_register()
else:
    st.sidebar.title(f"👤 {st.session_state.user}")

    menu = st.sidebar.radio("Menu", [
        "🌾 Crop Recommendation",
        "💧 Irrigation",
        "📊 Dashboard",
        "🚪 Logout"
    ])

    if menu == "🚪 Logout":
        st.session_state.user = None
        st.rerun()

    # ---------------- CROP ----------------
    elif menu == "🌾 Crop Recommendation":
        st.title("🌾 Crop Recommendation")

        N = st.number_input("Nitrogen", 0, 200, 90)
        P = st.number_input("Phosphorus", 0, 200, 42)
        K = st.number_input("Potassium", 0, 200, 43)
        temp = st.number_input("Temperature", 0.0, 50.0, 25.0)
        hum = st.number_input("Humidity", 0.0, 100.0, 80.0)
        ph = st.number_input("pH", 0.0, 14.0, 6.5)
        rain = st.number_input("Rainfall", 0.0, 500.0, 200.0)

        if st.button("Predict Crop"):
            data = [[N, P, K, temp, hum, ph, rain]]

            if crop_model:
                pred = crop_model.predict(data)[0]
            else:
                pred = "Rice (Demo)"

            st.success(f"🌾 Recommended Crop: {pred}")

    # ---------------- IRRIGATION ----------------
    elif menu == "💧 Irrigation":
        st.title("💧 Irrigation Prediction")

        t = st.number_input("Temperature", 0, 50, 25)
        h = st.number_input("Humidity", 0, 100, 50)
        m = st.number_input("Soil Moisture", 0, 100, 40)
        r = st.number_input("Rainfall", 0, 200, 50)

        if st.button("Predict Water"):
            data = [[t, h, m, r]]

            if irrigation_model:
                pred = irrigation_model.predict(data)[0]
            else:
                pred = (t*0.3 + h*0.2 + m*0.3 + r*0.2)

            st.success(f"💧 Water Needed: {round(pred,2)}")

    # ---------------- DASHBOARD ----------------
    elif menu == "📊 Dashboard":
        st.title("📊 Dashboard")

        st.plotly_chart(px.histogram(df, x="Temperature_C"))
        st.plotly_chart(px.histogram(df, x="Humidity"))
        st.plotly_chart(px.imshow(df.corr(numeric_only=True), text_auto=True))