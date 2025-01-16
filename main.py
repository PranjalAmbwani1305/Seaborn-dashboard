import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('covid_19_india.csv')

df['Date'] = pd.to_datetime(df['Date'])

st.title('COVID-19 Dashboard - India')

states = df['State/UnionTerritory'].unique()
selected_state = st.selectbox('Select a State:', states)

state_data = df[df['State/UnionTerritory'] == selected_state]

st.write(f"Showing data for {selected_state}")
st.write(state_data)

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=state_data, x='Date', y='Confirmed', ax=ax, marker='o', color='b')
ax.set_title(f'Time Series of Confirmed Cases in {selected_state}')
ax.set_xlabel('Date')
ax.set_ylabel('Confirmed Cases')
st.pyplot(fig)

st.write("Timeline of Confirmed, Recovered, and Death Cases")
state_data = state_data[['Date', 'Confirmed', 'Recovered', 'Deaths']]
st.write(state_data.set_index('Date'))
