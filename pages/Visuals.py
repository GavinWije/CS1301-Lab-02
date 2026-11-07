# Page for displaying data visualizations
import streamlit as st
import json
import pandas as pd
import os
import matplotlib as plt


current_dir = os.path.dirname(__file__)

st.set_page_config(
    page_title="Visuals",
    page_icon="📊"
)

st.title("Data Visualizations 📊")

# Graphs from data.json
st.subheader("Teen Phone Usage Data")

json_path = os.path.join(current_dir, "../data.json")
with open(json_path, "r") as f:
    json_data = json.load(f)

df_json = pd.DataFrame(json_data)
st.bar_chart(df_json, x="App", y="Average Hours Spent")


# Graphs from data.csv
csv_path = os.path.join(current_dir, "../data.csv")
df_csv = pd.read_csv(csv_path)
df_csv.columns = df_csv.columns.str.strip()

# Static + Advanced Charts
st.subheader("Height vs Weight")

fig, ax = plt.subplots()
ax.scatter(df_csv["Height"], df_csv["Weight"], color="steelblue")
ax.set_title("Height vs Weight")
ax.set_xlabel("Height (inches)")
ax.set_ylabel("Weight (lbs)")
st.pyplot(fig)

# Dynamic Charts
st.subheader("Explore Weight by Height (Interactive)")

# Keep a copy of the CSV data in session state so updates persist between interactions
if "csv_df" not in st.session_state:
    st.session_state["csv_df"] = df_csv.copy()

min_h = int(st.session_state["csv_df"]["Height"].min())
max_h = int(st.session_state["csv_df"]["Height"].max())
height_range = st.slider("Height range (inches):", min_h, max_h, (min_h, max_h))

new_height = st.number_input("Add a height (in):", min_value=36, max_value=96, value=66, step=1)
new_weight = st.number_input("Add a weight (lbs):", min_value=50, max_value=500, value=150, step=1)

if st.button("Add to chart"):
    new_row = pd.DataFrame({"Height": [new_height], "Weight": [new_weight]})
    st.session_state["csv_df"] = pd.concat([st.session_state["csv_df"], new_row], ignore_index=True)
    st.success("Point added!")

data = st.session_state["csv_df"]
shown = data[(data["Height"] >= height_range[0]) & (data["Height"] <= height_range[1])]
shown = shown.sort_values("Height")
st.line_chart(shown, x="Height", y="Weight")


# Interactive Session State 
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