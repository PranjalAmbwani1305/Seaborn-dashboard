import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the COVID-19 data
df = pd.read_csv('covid_19_india.csv')

# Convert 'Date' to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Set title for the dashboard
st.title('COVID-19 Dashboard - India')

# Get the list of unique states
states = df['State/UnionTerritory'].unique()
selected_state = st.selectbox('Select a State:', states)

# Filter the data for the selected state
state_data = df[df['State/UnionTerritory'] == selected_state]

# Create two columns for the layout
col1, col2 = st.columns(2)

# Plotting confirmed and death cases in the same graph in the first column
with col1:
    fig, ax = plt.subplots(figsize=(10, 5))
    
    sns.lineplot(data=state_data, x='Date', y='Confirmed', ax=ax, marker='o', color='b', label='Confirmed Cases')
    sns.lineplot(data=state_data, x='Date', y='Deaths', ax=ax, marker='o', color='r', label='Death Cases')
    
    ax.set_title(f'Time Series of Confirmed and Death Cases in {selected_state}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cases')
    
    # Use logarithmic scale for y-axis for better data visualization
    ax.set_yscale('log')
    
    ax.legend()  # Add legend to differentiate the lines
    st.pyplot(fig)

# Displaying the timeline data for confirmed and death cases in the second column
with col2:
    state_data_copy = state_data[['Date', 'Confirmed', 'Deaths']].copy()  # Create a copy to avoid overwriting original data
    st.write("Timeline of Confirmed and Death Cases")
    st.write(state_data_copy.set_index('Date'))

# Display additional details below
st.write(f"Showing data for {selected_state}")
st.write(state_data_copy)  # Display the modified data (with 'Confirmed' and 'Deaths' columns)
