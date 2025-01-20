import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from datetime import date

# Load and preprocess data
df = pd.read_csv('covid_19_india.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Streamlit Dashboard
st.title('COVID-19 Dashboard - India')

# State selection
states = df['State/UnionTerritory'].unique()
selected_state = st.selectbox('Select a State:', states)

# Filter data for the selected state
state_data = df[df['State/UnionTerritory'] == selected_state]

# Columns for visualization
col1, col2 = st.columns(2)

# Time Series Visualization
with col1:
    st.subheader(f'Time Series of Confirmed and Death Cases in {selected_state}')
    fig, ax = plt.subplots(figsize=(10, 5))
    
    sns.lineplot(data=state_data, x='Date', y='Confirmed', ax=ax, marker='o', color='b', label='Confirmed Cases')
    sns.lineplot(data=state_data, x='Date', y='Deaths', ax=ax, marker='o', color='r', label='Death Cases')
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Cases')
    ax.set_title(f'Time Series of Confirmed and Death Cases in {selected_state}')
    ax.set_yscale('log')
    ax.legend()
    st.pyplot(fig)

# Vertical Timeline Visualization
with col2:
    st.subheader('COVID-19 Key Events Timeline')
    
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
    
    fig, ax = plt.subplots(figsize=(5, 10))
    
    # Plot vertical timeline
    for i, (d, e) in enumerate(zip(dates, events)):
        y = len(events) - i - 1  # Reverse order for top-to-bottom timeline
        ax.plot([0, 1], [y, y], color='gray', linestyle='--', lw=1)
        ax.scatter(0.5, y, color='red', s=100, zorder=5)  # Event marker
        ax.text(0.6, y, e, fontsize=10, verticalalignment='center', horizontalalignment='left')  # Event label
        ax.text(-0.1, y, d.strftime('%b %Y'), fontsize=9, verticalalignment='center', horizontalalignment='right')  # Date

    # Styling
    ax.set_ylim(-1, len(events))
    ax.set_xlim(-0.2, 1.2)
    ax.axis('off')  # Remove axes for clean design
    ax.set_title('COVID-19 Key Events Timeline', fontsize=12, pad=20)

    st.pyplot(fig)

# Display state data
st.write(f"Showing data for {selected_state}")
state_data_display = state_data[['Date', 'Confirmed', 'Deaths']].set_index('Date')
st.write(state_data_display)
