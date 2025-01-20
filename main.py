import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta

# Load dataset
df = pd.read_csv('covid_19_india.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Set page config
st.set_page_config(
    page_title="COVID-19 Timeline App",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional styling
st.markdown("""
    <style>
        .main {background-color: #f5f5f5;}
        .sidebar .sidebar-content {background-color: #f0f0f5;}
        .stButton>button {background-color: #007BFF; color: white; font-size: 14px; padding: 10px; border-radius: 5px;}
        .stButton>button:hover {background-color: #0056b3;}
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📈 COVID-19 Timeline for States in India")
st.markdown("""
    This app provides an interactive timeline of COVID-19 cases for states in India.  
    Use the **filters** in the sidebar to explore the data.
""")

# Sidebar for user input
st.sidebar.title("Filters")
st.sidebar.markdown("Use the dropdown below to select a state:")
states = df['State/UnionTerritory'].unique()
selected_state = st.sidebar.selectbox("Select a State:", sorted(states))

# Filter data
state_data = df[df['State/UnionTerritory'] == selected_state]
state_data = state_data.sort_values(by='Date')

# Identify key dates dynamically
key_dates = state_data[
    (state_data['Confirmed'].diff().abs() > 1000) | 
    (state_data['Deaths'].diff().abs() > 100)
].copy()

# Layout with two columns
col1, col2 = st.columns([2, 1])  # Wider left column for charts

# Column 1: Time Series Chart
with col1:
    st.subheader(f"📊 Time Series for {selected_state}")
    fig, ax = plt.subplots(figsize=(12, 6))
    
    sns.lineplot(data=state_data, x='Date', y='Confirmed', ax=ax, label='Confirmed Cases', color='blue', marker='o')
    sns.lineplot(data=state_data, x='Date', y='Deaths', ax=ax, label='Death Cases', color='red', marker='o')
    
    ax.set_yscale('log')
    ax.set_title(f"COVID-19 Cases in {selected_state} (Log Scale)", fontsize=14, pad=15)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Number of Cases", fontsize=12)
    ax.legend(loc='upper left', fontsize=10)
    sns.despine()
    
    st.pyplot(fig)

# Column 2: Vertical Timeline
with col2:
    st.subheader("🗓️ Significant Events Timeline")
    if not key_dates.empty:
        fig, ax = plt.subplots(figsize=(5, 10))
        
        # Plot vertical timeline
        timeline_x = 0.5
        event_positions = range(len(key_dates))  # Evenly spaced positions
        ax.plot([timeline_x, timeline_x], [min(event_positions), max(event_positions)], 
                color='gray', linestyle='--', lw=1)
        
        # Add markers and labels
        for idx, (d, confirmed, deaths) in enumerate(zip(key_dates['Date'], key_dates['Confirmed'], key_dates['Deaths'])):
            ax.scatter(timeline_x, idx, color='red', s=100, zorder=5)
            label = f"{d.date()}\nConfirmed: {confirmed:,}\nDeaths: {deaths:,}"
            ax.text(timeline_x + 0.1, idx, label, fontsize=10, verticalalignment='center', horizontalalignment='left')
        
        # Style the plot
        ax.set_xlim(0.4, 0.6)
        ax.set_ylim(-1, len(key_dates) + 1)
        ax.axis('off')
        ax.set_title("Significant Events", fontsize=12, pad=20)
        st.pyplot(fig)
    else:
        st.write("No significant events detected for the selected state.")

# Full Table Section
st.markdown("---")
st.subheader(f"🧾 Full COVID-19 Data for {selected_state}")
state_data_display = state_data[['Date', 'Confirmed', 'Deaths']].set_index('Date')
st.dataframe(state_data_display.style.format("{:,}").highlight_max(axis=0, color="lightblue"))

