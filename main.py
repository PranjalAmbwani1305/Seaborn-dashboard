import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load dataset
df = pd.read_csv('covid_19_india.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Page title
st.set_page_config(page_title="City-Specific COVID-19 Timeline", layout="wide")
st.title("COVID-19 Timeline for a Selected City/State")

# Sidebar for city/state selection
st.sidebar.header("Filters")
states = df['State/UnionTerritory'].unique()
selected_state = st.sidebar.selectbox('Select a State:', states)

# Filter data for the selected state
state_data = df[df['State/UnionTerritory'] == selected_state]
state_data = state_data.sort_values(by='Date')

# Identify key dates dynamically (e.g., spikes in Confirmed or Death cases)
key_dates = state_data[
    (state_data['Confirmed'].diff().abs() > 1000) | 
    (state_data['Deaths'].diff().abs() > 100)
].copy()

# Create layout with two columns
col1, col2 = st.columns(2)

# Column 1: Time series visualization
with col1:
    st.subheader(f"Time Series of Confirmed and Death Cases in {selected_state}")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Plot Confirmed and Death cases over time
    sns.lineplot(data=state_data, x='Date', y='Confirmed', ax=ax, marker='o', color='b', label='Confirmed Cases')
    sns.lineplot(data=state_data, x='Date', y='Deaths', ax=ax, marker='o', color='r', label='Death Cases')
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Cases (Log Scale)')
    ax.set_yscale('log')  # Use log scale for better clarity
    ax.set_title(f"Time Series of COVID-19 Cases in {selected_state}")
    ax.legend()
    
    st.pyplot(fig)

# Column 2: Simple vertical timeline
with col2:
    st.subheader(f"Key Events Timeline for {selected_state}")
    if not key_dates.empty:
        fig, ax = plt.subplots(figsize=(6, 12))
        
        # Draw vertical timeline
        timeline_x = 0.5  # X-coordinate of the timeline
        event_y_positions = range(len(key_dates))  # Evenly spaced positions for events
        
        ax.plot([timeline_x, timeline_x], [min(event_y_positions), max(event_y_positions)], 
                color='gray', linestyle='--', lw=1)  # Timeline line
        
        # Add markers and labels
        for idx, (d, confirmed, deaths) in enumerate(zip(key_dates['Date'], key_dates['Confirmed'], key_dates['Deaths'])):
            # Marker for each event
            ax.scatter(timeline_x, idx, color='red', s=100, zorder=5)  # Event marker
            
            # Event label
            event_label = f"{d.date()}\nConfirmed: {confirmed:,}\nDeaths: {deaths:,}"
            ax.text(timeline_x + 0.1, idx, event_label, fontsize=9, verticalalignment='center', horizontalalignment='left')
        
        # Format the plot
        ax.set_xlim(0.4, 0.6)
        ax.set_ylim(min(event_y_positions) - 1, max(event_y_positions) + 1)
        ax.axis('off')
        ax.set_title("Significant Case Updates Timeline", fontsize=12, pad=20)
        
        st.pyplot(fig)
    else:
        st.write("No significant events detected for the selected state.")

# Display the filtered data in a table
st.write(f"### COVID-19 Data for {selected_state}")
state_data_display = state_data[['Date', 'Confirmed', 'Deaths']].set_index('Date')
st.dataframe(state_data_display)
