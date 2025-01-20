import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset
df = pd.read_csv('covid_19_india.csv')
df['Date'] = pd.to_datetime(df['Date'])

# Page configuration
st.set_page_config(page_title="COVID-19 Dashboard - Timeline", layout="wide")
st.title("COVID-19 Timeline - India")

# Sidebar for state selection
st.sidebar.header("Filters")
states = df['State/UnionTerritory'].unique()
selected_state = st.sidebar.selectbox('Select a State:', states)

# Filter data for the selected state
state_data = df[df['State/UnionTerritory'] == selected_state]
state_data = state_data.sort_values('Date')  # Ensure data is sorted by date

# Vertical timeline visualization
st.subheader(f"Vertical Timeline of Confirmed and Death Cases in {selected_state}")

# Prepare data for the timeline
timeline_data = state_data[['Date', 'Confirmed', 'Deaths']].copy()
timeline_data = timeline_data[timeline_data['Confirmed'] > 0]  # Remove rows with no cases
timeline_data['Event'] = (
    "Confirmed: " + timeline_data['Confirmed'].astype(str) +
    ", Deaths: " + timeline_data['Deaths'].astype(str)
)

# Plot the vertical timeline
fig, ax = plt.subplots(figsize=(5, 15))

# Draw timeline lines
x = 0.5
ax.plot([x] * len(timeline_data), timeline_data['Date'], color='gray', linestyle='--', lw=1)

# Add points and labels for each event
for d, e in zip(timeline_data['Date'], timeline_data['Event']):
    ax.scatter(x, d, color='blue', s=100, zorder=5)
    ax.text(x + 0.05, d, e, fontsize=10, verticalalignment='center', horizontalalignment='left')

# Customize the plot
ax.set_xlim(0, 1)
ax.set_ylim(timeline_data['Date'].min() - pd.Timedelta(days=30), timeline_data['Date'].max() + pd.Timedelta(days=30))
ax.axis('off')
ax.set_title(f"COVID-19 Timeline for {selected_state}", fontsize=12, pad=20)

# Display the plot
st.pyplot(fig)

# Display the underlying data as a table
st.write(f"### Timeline Data for {selected_state}")
st.dataframe(timeline_data.set_index('Date'))
