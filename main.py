import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import date

df = pd.read_csv('covid_19_india.csv')
df['Date'] = pd.to_datetime(df['Date'])

st.title('COVID-19 Dashboard - India')

states = df['State/UnionTerritory'].unique()
selected_state = st.selectbox('Select a State:', states)

state_data = df[df['State/UnionTerritory'] == selected_state]

col1, col2 = st.columns(2)

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

with col2:
    st.subheader('COVID-19 Key Events Timeline')
    
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
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    for i, (d, e) in enumerate(zip(dates, events)):
        ax.plot([d, d], [0, 1], color='gray', linestyle='--', lw=1)
        ax.text(d, 1.05, e, rotation=45, ha='right', va='bottom', fontsize=10)
    
    ax.scatter(dates, [1] * len(dates), color='red', s=50, label='Events')
    ax.set_ylim(0, 1.5)
    ax.set_xlim(min(dates) - pd.Timedelta(days=30), max(dates) + pd.Timedelta(days=30))
    
    ax.set_title('COVID-19 Key Events Timeline')
    ax.set_yticks([])
    ax.set_xlabel('Date')
    ax.legend()

    st.pyplot(fig)

st.write(f"Showing data for {selected_state}")
state_data_display = state_data[['Date', 'Confirmed', 'Deaths']].set_index('Date')
st.write(state_data_display)
