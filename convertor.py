import streamlit as st
import pandas as pd
import plotly.express as px

# Custom CSS
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #1f1c2c, #928dab);
            color: #ffffff;
        }
        .stApp {
            background: linear-gradient(135deg, #1f1c2c, #928dab);
            color: white;
        }
        .stTextInput, .stNumberInput, .stSelectbox {
            background-color: #2c2c54;
            color: #ffffff;
            border-radius: 10px;
            padding: 8px;
        }
        .stButton>button {
            background-color: #3498db;
            color: white;
            border-radius: 12px;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #2980b9;
            transform: scale(1.05);
        }
        .stSuccess {
            background-color: #00e676;
            color: white;
            padding: 12px;
            border-radius: 12px;
            font-weight: bold;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Conversion factors
data = {
    "Length": {"meter": 1, "kilometer": 0.001, "centimeter": 100, "mile": 0.000621371},
    "Weight": {"kilogram": 1, "gram": 1000, "pound": 2.20462, "ounce": 35.274},
    "Temperature": {"Celsius": "C", "Fahrenheit": "F", "Kelvin": "K"},
}

df = {category: pd.DataFrame(list(units.items()), columns=["Unit", "Factor"]) for category, units in data.items() if category != "Temperature"}

def convert(value, from_unit, to_unit, category):
    if category == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
        else:
            return value
    else:
        return value * data[category][to_unit] / data[category][from_unit]

st.title("🚀 Stylish Unit Converter")
st.write("💡 Made by Anabia")

category = st.selectbox("📌 Select Category", list(data.keys()))

if category == "Temperature":
    from_unit = st.selectbox("🌡️ From Unit", list(data[category].keys()))
    to_unit = st.selectbox("🌡️ To Unit", list(data[category].keys()))
else:
    from_unit = st.selectbox("📏 From Unit", df[category]["Unit"].tolist())
    to_unit = st.selectbox("📏 To Unit", df[category]["Unit"].tolist())

value = st.number_input("✏️ Enter Value", min_value=0.0, format="%.2f")
converted_value = convert(value, from_unit, to_unit, category)
st.success(f"✅ Converted Value: {converted_value} {to_unit}")

# Plotly Visualization
if category != "Temperature":
    fig = px.bar(df[category], x="Unit", y="Factor", title=f"📊 Conversion Factors for {category}", color="Unit")
    st.plotly_chart(fig)
