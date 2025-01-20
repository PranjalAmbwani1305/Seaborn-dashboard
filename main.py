import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta

# Load dataset
df = pd.read_csv('covid_19_india.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Set page configuration
st.set_page_config(page_title="COVID-19 Vertical Timeline", layout="wide")
st.title("🗓️ COVID-19 Vertical Timeline of Significant Events")

# Sidebar for state selection
st.sidebar.title("Filters")
states = sorted(df['State/UnionTerritory'].unique())
selected_state = st.sidebar.selectbox("Select a State:", states)

# Filter data for the selected state
state_data = df[df['State/UnionTerritory'] == selected_state].sort_values(by="Date")

# Identify key dates (spikes in confirmed or death cases)
key_dates = state_data[
    (state_data['Confirmed'].diff().abs() > 1000) |
    (state_data['Deaths'].diff().abs() > 100)
].copy()

# Check if there are significant events
if key_dates.empty:
    st.write("No significant events found for the selected state.")
else:
    # Limit number of key dates plotted (optional)
    max_events = 50  # Adjust this number based on your data and needs
    key_dates = key_dates.head(max_events)

    # Prepare data for the timeline
    key_dates['Event'] = key_dates.apply(
        lambda row: f"Date: {row['Date'].strftime('%Y-%m-%d')}\nConfirmed: {row['Confirmed']:,}\nDeaths: {row['Deaths']:,}",
        axis=1
    )

    # Debugging step: Check if there are events in the timeline
    st.write(f"Total number of events: {len(key_dates)}")

    # Create a vertical timeline
    st.subheader(f"Significant Events in {selected_state}")
    
    # Check if the number of events is reasonable for display
    if len(key_dates) > 0:
        fig, ax = plt.subplots(figsize=(5, min(len(key_dates) * 1.5, 20)))  # Limit height to a reasonable size

        # Draw the timeline line
        ax.vlines(0, 0, len(key_dates) - 1, color='gray', linestyles='dashed', lw=1)

        # Plot event markers and labels
        for i, (date, event) in enumerate(zip(key_dates['Date'], key_dates['Event'])):
            ax.scatter(0, i, color='red', s=100, zorder=5)
            ax.text(0.2, i, event, fontsize=10, verticalalignment='center', horizontalalignment='left')

        # Remove axes for a clean look
        ax.axis('off')
        ax.set_ylim(-1, len(key_dates))
        ax.set_title("Timeline of Significant COVID-19 Events", fontsize=14, pad=20)

        # Display the plot
        st.pyplot(fig)
    else:
        st.write("No events to display in the timeline.")
