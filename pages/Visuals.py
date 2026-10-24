# This creates the page for displaying data visualizations.
import streamlit as st
import json
import pandas as pd
import os

# Get the directory where Visuals.py is currently located
current_dir = os.path.dirname(__file__)

st.set_page_config(
    page_title="Visuals",
    page_icon="📊"
)

st.title("Data Visualizations 📊")

# PART 1: GRAPHS FROM data.json
st.subheader("Teen Phone Usage Data")

json_path = os.path.join(current_dir, "../data.json")
with open(json_path, "r") as f:
    json_data = json.load(f)

df_json = pd.DataFrame(json_data)
st.bar_chart(df_json, x="App", y="Average Hours Spent")


# PART 2: GRAPHS FROM data.csv 
st.subheader("Income by Educational Attainment")

csv_path = os.path.join(current_dir, "../data.csv")
df_csv = pd.read_csv(csv_path)

# Clean up any accidental whitespace in column names
df_csv.columns = df_csv.columns.str.strip()

# Display the line or bar chart
st.bar_chart(df_csv, x="Educational Attainment", y="Medium Weekly Income")


# PART 3: INTERACTIVE SESSION STATE 
st.subheader("Interactive Data Updater")

if "chart_data" not in st.session_state:
    st.session_state["chart_data"] = {
        "App": ["Streaming Video", "Social Media", "Social Gaming"],
        "Hours": [3.0, 2.5, 2.0]
    }

new_app = st.text_input("Enter new App name:")
new_hours = st.number_input("Enter hours spent:", min_value=0.0, max_value=24.0, step=0.5)

if st.button("Add Data Point"):
    if new_app:
        st.session_state["chart_data"]["App"].append(new_app)
        st.session_state["chart_data"]["Hours"].append(new_hours)
        st.success(f"Added {new_app}!")

df_interactive = pd.DataFrame(st.session_state["chart_data"])
st.bar_chart(df_interactive, x="App", y="Hours")