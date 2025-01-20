import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

# Load dataset
df = pd.read_csv('covid_19_india.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Set page configuration
st.set_page_config(page_title="COVID-19 Professional Timeline", layout="wide")

# Sidebar for user input
st.sidebar.title("Filters")
states = sorted(df['State/UnionTerritory'].unique())
selected_state = st.sidebar.selectbox("Select a State:", states)

# Filter data
state_data = df[df['State/UnionTerritory'] == selected_state].sort_values(by="Date")
key_dates = state_data[
    (state_data['Confirmed'].diff().abs() > 1000) |
    (state_data['Deaths'].diff().abs() > 100)
].copy()

# Timeline Layout
st.title(f"🗓️ COVID-19 Timeline for {selected_state}")
if key_dates.empty:
    st.write("No significant events found for the selected state.")
else:
    fig, ax = plt.subplots(figsize=(5, 10))

    # Create a vertical timeline
    timeline_dates = key_dates['Date']
    timeline_labels = [
        f"Date: {d.strftime('%Y-%m-%d')}\nConfirmed: {c:,}\nDeaths: {dc:,}"
        for d, c, dc in zip(key_dates['Date'], key_dates['Confirmed'], key_dates['Deaths'])
    ]
    
    # Dynamic positions to avoid overlap
    y_positions = range(len(timeline_dates))  # Space out the labels evenly
    ax.plot([0.5, 0.5], [0, len(timeline_dates) - 1], color='gray', lw=1, linestyle="--")

    # Add event markers and labels
    for idx, (label, y_pos) in enumerate(zip(timeline_labels, y_positions)):
        ax.scatter(0.5, y_pos, color='red', s=100, zorder=5)
        ax.text(0.55, y_pos, label, fontsize=9, verticalalignment='center', horizontalalignment='left')

    # Remove axis and set limits
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(-1, len(timeline_dates))
    ax.set_title("Significant COVID-19 Events", fontsize=14, pad=10)
    
    st.pyplot(fig)
