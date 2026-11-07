# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.
import csv
import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    height_input = st.number_input("Your height (inches):", min_value=36, max_value=96, value=66, step=1)
    weight_input = st.number_input("Your weight (lbs):", min_value=50, max_value=500, value=150, step=1)
    submitted = st.form_submit_button("Submit Data")

    if submitted:
        with open("data.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([height_input, weight_input])
        st.success("Your data has been submitted!")
        st.write(f"You entered: **Height:** {height_input} in, **Weight:** {weight_input} lbs")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")