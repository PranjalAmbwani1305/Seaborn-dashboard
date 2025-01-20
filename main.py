import matplotlib.pyplot as plt
from datetime import date

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

# Create a vertical timeline graph
fig, ax = plt.subplots(figsize=(5, 8))  # Adjust figure size for better visibility

# Plot each event
for i, (d, e) in enumerate(zip(dates, events)):
    y = len(events) - i - 1  # Reverse the order for a top-to-bottom timeline
    ax.plot([0.5, 0.5], [y - 0.4, y + 0.4], color='gray', linestyle='--', lw=1)  # Vertical connecting lines
    ax.scatter(0.5, y, color='red', s=100, zorder=5)  # Event marker
    ax.text(0.55, y, e, fontsize=10, verticalalignment='center', horizontalalignment='left')  # Event label
    ax.text(0.45, y, d.strftime('%b %Y'), fontsize=9, verticalalignment='center', horizontalalignment='right')  # Date

# Style the chart
ax.set_ylim(-1, len(events))
ax.set_xlim(0, 1)
ax.axis('off')  # Hide the axes
ax.set_title('COVID-19 Key Events Timeline', fontsize=14, pad=20)

# Show the plot
plt.tight_layout()
plt.show()
