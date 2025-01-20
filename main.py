import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
df = pd.read_csv('covid_19_india.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Example: Add an additional DataFrame for events and dates (replace this with your actual source)
events_df = pd.DataFrame({
    'Date': pd.to_datetime(['2020-01-30', '2020-03-24', '2021-01-16', '2022-04-01']),
    'Event': ['First COVID-19 Case in India', 'National Lockdown Starts', 'Vaccination Begins', 'Relaxation of Restrictions']
})

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

# Column 2: Vertical timeline
with col2:
    st.subheader("COVID-19 Key Events Timeline")
    
    # Sort events by date
    events_df = events_df.sort_values('Date')
    
    # Create a vertical timeline
    fig, ax = plt.subplots(figsize=(5, 10))
    x = 0.5  # Horizontal position of the timeline
    ax.plot([x] * len(events_df), events_df['Date'], color='gray', linestyle='--', lw=1)  # Timeline line
    
    for d, e in zip(events_df['Date'], events_df['Event']):
        ax.scatter(x, d, color='red', s=100, zorder=5)  # Event marker
        ax.text(x + 0.05, d, e, fontsize=10, verticalalignment='center', horizontalalignment='left')  # Event label
    
    # Remove axes and style the chart
    ax.set_xlim(0, 1)
    ax.set_ylim(events_df['Date'].min() - pd.Timedelta(days=30), events_df['Date'].max() + pd.Timedelta(days=30))
    ax.axis('off')
    ax.set_title('COVID-19 Key Events Timeline', fontsize=12, pad=20)

    st.pyplot(fig)

# Additional table section
st.write(f"### COVID-19 Data for {selected_state}")
state_data_display = state_data[['Date', 'Confirmed', 'Deaths']].set_index('Date')
st.dataframe(state_data_display)

