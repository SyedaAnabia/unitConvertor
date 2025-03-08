import streamlit as st
import pandas as pd
import plotly.express as px

# Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stApp {
            background-color: #0e1117;
        }
        .stTextInput, .stNumberInput, .stSelectbox {
            background-color: #1c1f26;
            color: #ffffff;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #ff7878;
        }
        .stSuccess {
            background-color: #00c853;
            color: white;
            padding: 10px;
            border-radius: 10px;
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

st.title("🔄 Unit Converter")
st.write("Made by Noman")

category = st.selectbox("Select Category", list(data.keys()))

if category == "Temperature":
    from_unit = st.selectbox("From Unit", list(data[category].keys()))
    to_unit = st.selectbox("To Unit", list(data[category].keys()))
else:
    from_unit = st.selectbox("From Unit", df[category]["Unit"].tolist())
    to_unit = st.selectbox("To Unit", df[category]["Unit"].tolist())

value = st.number_input("Enter Value", min_value=0.0, format="%.2f")
converted_value = convert(value, from_unit, to_unit, category)
st.success(f"Converted Value: {converted_value} {to_unit}")

# Plotly Visualization
if category != "Temperature":
    fig = px.bar(df[category], x="Unit", y="Factor", title=f"Conversion Factors for {category}")
    st.plotly_chart(fig)
