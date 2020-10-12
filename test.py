import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import Functions.kpi as d

days = range(1, len(d.strike_days1) + 1, 1)
ypos=np.arange(len(d.strike_days1))
y = range(len(d.strike_rate))

fig, ax = plt.subplots(figsize=(12.81, 4.8))
plt.ylim(0, 101, 10)
line = plt.plot(d.strike_rate, color='green', linewidth='4',  marker='D', markerfacecolor="red")

# Show data point ----------------------------------------
for i, v in enumerate(d.strike_rate):
    ax.text(i, v+3, "%d" %v, ha="center", fontsize='14')

ax.set_xticks(ypos)
ax.set_xticklabels(d.strike_days1, fontsize=14)

plt.title('03. Day wise Strike Days', fontsize=16, fontweight='bold', color='#3e0a75')
plt.xlabel('Days', fontsize='14', color='black', fontweight='bold')
plt.ylabel('Strike Rate %', fontsize='14', color='black', fontweight='bold')
plt.legend(['Strike Rate'], loc='upper right', fontsize='14')
# plt.show()
plt.savefig('./Images/day_-wise_strike_rate.png')