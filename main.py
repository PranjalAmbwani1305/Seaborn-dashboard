import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
    st.subheader("Task Timeline")
    task_df = pd.DataFrame({
        "Task": ["Task 1", "Task 2", "Task 3"],
        "Start": [0, 2, 5],
        "Duration": [3, 4, 2]
    })
    sns.set_style("whitegrid")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    for idx in range(len(task_df)):
        task = task_df["Task"][idx]
        start = task_df["Start"][idx]
        duration = task_df["Duration"][idx]
        
        ax.plot([start, start + duration], [task, task], marker='o', color='skyblue', markersize=8, linewidth=4)
        
    ax.set_xlabel("Time (Days)")
    ax.set_ylabel("Task")
    ax.set_title("Task Timeline")
    ax.set_ylim(-1, len(task_df))  # Adjust to fit all tasks
    ax.set_xticks(range(0, max(task_df['Start'] + task_df['Duration']), 1))
    ax.set_xlim(0, max(task_df['Start'] + task_df['Duration']) + 1)
    
    st.pyplot(fig)

st.write(f"Showing data for {selected_state}")
state_data_display = state_data[['Date', 'Confirmed', 'Deaths']].set_index('Date')
st.write(state_data_display)
