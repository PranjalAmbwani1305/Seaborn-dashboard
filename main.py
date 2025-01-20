import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date

# Load the dataset
df = pd.read_csv('covid_19_india.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Page title
st.set_page_config(page_title="COVID-19 Dashboard - India", layout="wide")
st.title("COVID-19 Dashboard - India")

# Sidebar for state selection
st.sidebar.header("Filters")
states = df['State/UnionTerritory'].unique()
selected_state = st.sidebar.selectbox('Select a State:', states)

# Filter data for the selected state
state_data = df[df['State/UnionTerritory'] == selected_state]

# Create two columns
col1, col2 = st.columns(2)

# Column 1: Time series visualization
with col1:
    st.subheader(f"Time Series of Confirmed and Death Cases in {selected_state}")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot confirmed and death cases
    sns.lineplot(data=state_data, x='Date', y='Confirmed', ax=ax, marker='o', color='b', label='Confirmed Cases')
    sns.lineplot(data=state_data, x='Date', y='Deaths', ax=ax, marker='o', color='r', label='Death Cases')
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Cases (Log Scale)')
    ax.set_yscale('log')  # Logarithmic scale for better visualization
    ax.set_title(f"Time Series of COVID-19 Cases in {selected_state}")
    ax.legend()
    
    st.pyplot(fig)

# Column 2: Horizontal timeline
with col2:
    st.subheader("COVID-19 Key Events Timeline")
    
    # Event dates and descriptions
    dates = [
        date(2020, 1, 30),
        date(2020, 3, 24),
        date(2021, 1, 16),
        date(2022, 4, 1)
    ]
    events = [
        'First COVID-19 Case in India',
        'National Lockdown Starts',
        'Vaccination Begins',
        'Relaxation of Restrictions'
    ]
    
    # Create a horizontal timeline
    fig, ax = plt.subplots(figsize=(10, 3))
    y = 0.5  # Vertical position of the timeline
    ax.plot(dates, [y] * len(dates), color='gray', linestyle='--', lw=1)  # Timeline line
    
    for d, e in zip(dates, events):
        ax.scatter(d, y, color='red', s=100, zorder=5)  # Event marker
        ax.text(d, y + 0.05, e, fontsize=10, verticalalignment='bottom', horizontalalignment='center', rotation=45)  # Event label
    
    # Remove axes and style the chart
    ax.set_ylim(0, 1)
    ax.set_xlim(min(dates) - pd.Timedelta(days=30), max(dates) + pd.Timedelta(days=30))
    ax.axis('off')
    ax.set_title('COVID-19 Key Events Timeline', fontsize=12, pad=20)

    st.pyplot(fig)

# Additional table section
st.write(f"### COVID-19 Data for {selected_state}")
state_data_display = state_data[['Date', 'Confirmed', 'Deaths']].set_index('Date')
st.dataframe(state_data_display)

# Footer section
st.markdown(
    """
    ---
    **Created with ❤️ using Streamlit**
    """
)
