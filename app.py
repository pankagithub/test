import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.express as px
import os 

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="SegmenTrack", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## 🚀 SegmenTrack")

# 🌙 THEME TOGGLE
theme = st.sidebar.toggle("🌙 Dark Mode", value=True)

# Theme Variables
if theme:
    bg_color = "#0e1117"
    card_color = "#111827"
    text_color = "white"
    accent = "#00ffcc"
    chart_template = "plotly_dark"
else:
    bg_color = "#f5f5f5"
    card_color = "#ffffff"
    text_color = "#000000"
    accent = "#007bff"
    chart_template = "plotly_white"

# ---------------- CUSTOM CSS ----------------
st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
}}
.main {{
    background-color: {bg_color};
}}
.card {{
    background-color: {card_color};
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: {text_color};
    box-shadow: 0 0 10px rgba(0,0,0,0.2);
}}
.metric-title {{
    font-size: 14px;
    color: gray;
}}
.metric-value {{
    font-size: 26px;
    font-weight: bold;
    color: {accent};
}}
.title {{
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: {accent};
}}
</style>
""", unsafe_allow_html=True)

# ---------------- MENU ----------------
menu = ["🏠 Dashboard", "📂 Upload Data", "🔮 Predict"]
choice = st.sidebar.radio("Menu", menu)

# ---------------- FILTERS ----------------
st.sidebar.markdown("### 🔍 Filters")
region = st.sidebar.multiselect("Region", ["East", "West", "North", "South"])
location = st.sidebar.multiselect("Location", ["Urban", "Rural"])
construction = st.sidebar.multiselect("Construction", ["Frame", "Masonry", "Fire Resist"])

# ---------------- LOAD MODEL ----------------
if os.path.exists("C:/Users/Pankaj/Desktop/Himanshu-Kori(Datasem-10)_GUJARAT-UNIVERSITY_SegmentTrack/Himanshu-Kori(Datasem-10)_GUJARAT-UNIVERSITY_SegmentTrack/model.pkl") and os.path.exists("scaler.pkl"):
    model = pickle.load(open("model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
else:
    model = None
    scaler = None

# ---------------- TITLE ----------------
st.markdown(f'<p class="title">📊 SegmenTrack Dashboard</p>', unsafe_allow_html=True)

# ---------------- FILE READER FUNCTION (IMPORTANT: TOP PAR) ----------------
def load_file(file):
    try:
        if file.name.endswith(".csv"):
            try:
                return pd.read_csv(file)
            except:
                return pd.read_csv(file, encoding="latin1")

        elif file.name.endswith(".xlsx") or file.name.endswith(".xls"):
            return pd.read_excel(file)

        elif file.name.endswith(".xml"):
            return pd.read_xml(file)

        else:
            return None
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None


# ---------------- DASHBOARD ----------------
if choice == "🏠 Dashboard":

    df = pd.DataFrame({
        "Policy": np.random.randint(100000, 200000, 20),
        "Region": np.random.choice(["East", "West", "North", "South"], 20),
        "Location": np.random.choice(["Urban", "Rural"], 20),
        "Construction": np.random.choice(["Frame", "Masonry", "Fire Resist"], 20),
        "Investment": np.random.randint(100000, 10000000, 20),
        "Rating": np.random.uniform(1, 10, 20).round(1)
    })

    # ✅ APPLY FILTERS
    filtered_df = df.copy()

    if region:
        filtered_df = filtered_df[filtered_df["Region"].isin(region)]

    if location:
        filtered_df = filtered_df[filtered_df["Location"].isin(location)]

    if construction:
        filtered_df = filtered_df[filtered_df["Construction"].isin(construction)]

    st.markdown("### 📋 Data Overview")
    st.dataframe(filtered_df, use_container_width=True)

    if filtered_df.empty:
        st.warning("No data available for selected filters ⚠️")
    else:
        col1, col2, col3, col4, col5 = st.columns(5)

        col1.markdown(f"""
        <div class="card">
            <div class="metric-title">Total Investment</div>
            <div class="metric-value">{filtered_df['Investment'].sum():,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="card">
            <div class="metric-title">Most Frequent</div>
            <div class="metric-value">{filtered_df['Investment'].mode()[0]}</div>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="card">
            <div class="metric-title">Average</div>
            <div class="metric-value">{filtered_df['Investment'].mean():,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        col4.markdown(f"""
        <div class="card">
            <div class="metric-title">Median</div>
            <div class="metric-value">{filtered_df['Investment'].median():,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        col5.markdown(f"""
        <div class="card">
            <div class="metric-title">Ratings</div>
            <div class="metric-value">{filtered_df['Rating'].sum():.2f}</div>
        </div>
        """, unsafe_allow_html=True)

        # Charts
        st.markdown("### 📊 Visual Insights")

        col1, col2 = st.columns(2)

        fig_bar = px.bar(filtered_df, x="Region", y="Investment", color="Region", template=chart_template)
        col1.plotly_chart(fig_bar, use_container_width=True)

        fig_pie = px.pie(filtered_df, names="Location", template=chart_template)
        col2.plotly_chart(fig_pie, use_container_width=True)

        col3, col4 = st.columns(2)

        fig_line = px.line(filtered_df, x="Policy", y="Investment", template=chart_template)
        col3.plotly_chart(fig_line, use_container_width=True)

        fig_hist = px.histogram(filtered_df, x="Investment", template=chart_template)
        col4.plotly_chart(fig_hist, use_container_width=True)


# ========================= UPLOAD =========================
elif choice == "📂 Upload Data":

    st.markdown("## 📂 Upload Dataset")

    file = st.file_uploader("Upload File", type=["csv", "xlsx", "xls", "xml"])

    if file:
        df = load_file(file)

        if df is None:
            st.error("Unsupported or broken file")
            st.stop()

        # CLEAN COLUMNS
        df.columns = df.columns.str.strip()

        st.write("### 🔍 Columns")
        st.write(df.columns)

        st.write("### 📊 Preview")
        st.dataframe(df.head())

        # -------- COLUMN SELECTION --------
        st.markdown("### ⚙️ Select Columns")

        col1, col2 = st.columns(2)
        quantity_col = col1.selectbox("Quantity Column", df.columns)
        price_col = col2.selectbox("Price Column", df.columns)

        # SAFE CALCULATION
        df["TotalPrice"] = pd.to_numeric(df[quantity_col], errors='coerce') * \
                           pd.to_numeric(df[price_col], errors='coerce')

        # OPTIONAL
        customer_col = st.selectbox("Customer Column", ["None"] + list(df.columns))
        invoice_col = st.selectbox("Invoice Column", ["None"] + list(df.columns))
        country_col = st.selectbox("Country Column", ["None"] + list(df.columns))

        # -------- METRICS --------
        st.markdown("### 📊 Metrics")

        col1, col2, col3 = st.columns(3)

        revenue = df["TotalPrice"].sum()
        customers = df[customer_col].nunique() if customer_col != "None" else 0
        orders = df[invoice_col].nunique() if invoice_col != "None" else 0

        col1.metric("Revenue", f"{revenue:,.0f}")
        col2.metric("Customers", customers)
        col3.metric("Orders", orders)

        # -------- CHARTS --------
        st.markdown("### 📈 Visual Insights")

        col1, col2 = st.columns(2)

        fig1 = px.scatter(df, x=quantity_col, y=price_col,
                          color=country_col if country_col != "None" else None,
                          template=chart_template)
        col1.plotly_chart(fig1, use_container_width=True)

        if country_col != "None":
            fig2 = px.pie(df, names=country_col, template=chart_template)
            col2.plotly_chart(fig2, use_container_width=True)

        # INFO
        st.markdown("### 📌 Dataset Info")
        st.write("Shape:", df.shape)
# ---------------- PREDICT ----------------
elif choice == "🔮 Predict":

    st.markdown("## 🔮 Predict Customer Segment")

    if model is None:
        st.error("Model not found!")
    else:
        col1, col2, col3 = st.columns(3)

        recency = col1.number_input("Recency", 0, 500)
        frequency = col2.number_input("Frequency", 0, 1000)
        monetary = col3.number_input("Monetary", 0.0, 100000.0)

        if st.button("Predict"):

            #  FIXED (NO WARNING)
            input_df = pd.DataFrame({
                "Recency": [recency],
                "Frequency": [frequency],
                "Monetary": [monetary]
            })

            data_scaled = scaler.transform(input_df)
            prediction = model.predict(data_scaled)[0]

            segment_map = {
                0: "Low Value",
                1: "High Value",
                2: "Medium Value",
                3: "Premium Customer"
            }

            st.success(f"🎯 Segment: {segment_map.get(prediction)}")

            st.dataframe(input_df)

            df = pd.DataFrame({
                "Feature": ["Recency", "Frequency", "Monetary"],
                "Value": [recency, frequency, monetary]
            })

            st.markdown("### 📊 Visual Insights")

            col1, col2 = st.columns(2)

            fig_bar = px.bar(df, x="Feature", y="Value", color="Feature", template=chart_template)
            col1.plotly_chart(fig_bar, use_container_width=True)

            fig_pie = px.pie(df, names="Feature", values="Value", template=chart_template)
            col2.plotly_chart(fig_pie, use_container_width=True)

            col3, col4 = st.columns(2)

            fig_line = px.line(df, x="Feature", y="Value", markers=True, template=chart_template)
            col3.plotly_chart(fig_line, use_container_width=True)

            fig_hist = px.histogram(df, x="Value", template=chart_template)
            col4.plotly_chart(fig_hist, use_container_width=True)

            st.markdown("### 🔍 Correlation View")
            fig_scatter = px.scatter(df, x="Feature", y="Value", size="Value", color="Feature", template=chart_template)
            st.plotly_chart(fig_scatter, use_container_width=True)


















