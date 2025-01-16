import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data():
    df = pd.read_csv('covid_19_india.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    return df

# Load data
df = load_data()

st.sidebar.title("State Filter")
selected_state = st.sidebar.selectbox("Select a state", df['State'].unique())

filtered_data = df[df['State'] == selected_state]

st.title(f"COVID-19 Dashboard for {selected_state}")

# Confirmed Cases Over Time
st.header("Confirmed Cases Over Time")
plt.figure(figsize=(10, 6))
sns.lineplot(x='Date', y='Confirmed', data=filtered_data, marker='o', label="Confirmed Cases")
plt.title(f"Confirmed Cases Over Time for {selected_state}")
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt)

# Deaths Over Time
st.header(f"Deaths Over Time for {selected_state}")
plt.figure(figsize=(10, 6))
sns.lineplot(x='Date', y='Deaths', data=filtered_data, marker='o', color='red', label="Deaths")
plt.title(f"Deaths Over Time for {selected_state}")
plt.xlabel('Date')
plt.ylabel('Deaths')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt)
