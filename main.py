import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('covid_19_india.csv')
print(data.columns())
df['Date'] = pd.to_datetime(df['Date'])

st.title('COVID-19 Dashboard - India')

states = df['State/UnionTerritory'].unique()
selected_state = st.selectbox('Select a State:', states)

state_data = df[df['State/UnionTerritory'] == selected_state]

st.write(f"Showing data for {selected_state}")
st.write(state_data)

# Create two columns for side-by-side display (Top Row)
col1, col2 = st.columns(2)

# Plot the graph in the first column
with col1:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=state_data, x='Date', y='Confirmed', ax=ax, marker='o', color='b')
    ax.set_title(f'Time Series of Confirmed Cases in {selected_state}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Confirmed Cases')
    st.pyplot(fig)

# Display the timeline in the second column
with col2:
    # Check if 'Recovered' column exists or handle missing columns
    columns_to_check = ['Date', 'Confirmed', 'Recovered', 'Deaths']
    missing_columns = [col for col in columns_to_check if col not in state_data.columns]

    if missing_columns:
        st.error(f"Missing columns: {', '.join(missing_columns)}")
        # Skip the missing 'Recovered' column if it does not exist
        if 'Recovered' not in state_data.columns:
            state_data = state_data[['Date', 'Confirmed', 'Deaths']]
    else:
        state_data = state_data[columns_to_check]

    st.write("Timeline of Confirmed, Recovered, and Death Cases")
    st.write(state_data.set_index('Date'))

# Display the table below the graph and timeline (Bottom Row)
st.write("Full Data Table")
st.write(state_data.set_index('Date'))
