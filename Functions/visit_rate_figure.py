
import matplotlib.pyplot as plt
import math
import Functions.all_functions as fn
import numpy as np

def day_wise_visit_rate(visit_days, day_visit_rate):
    range(1, len(visit_days) + 1, 1)
    ypos = np.arange(len(visit_days))

    avg = []
    for i in range(len(day_visit_rate)):
        a = sum(day_visit_rate) / len(day_visit_rate)
        avg.append(a)

    fig, ax = plt.subplots(figsize=(12.81, 4.8))
    plt.ylim(0, 101, 10)
    plt.plot(day_visit_rate, color='#007cff', linewidth='3', marker='D', markerfacecolor="#fcff00")
    plt.plot(avg, color='#c3bdbd', linestyle='--', linewidth='2')

    # Show data point ----------------------------------------------
    for i, v in enumerate(day_visit_rate):
        ax.text(i, v + 3, str(v) + '%', ha="center", fontsize='14')

    ax.set_xticks(ypos)
    ax.set_xticklabels(visit_days, fontsize=14)

    plt.title('03. Day wise Visit Rate', fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Days', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('Visit Rate %', fontsize='14', color='black', fontweight='bold')
    plt.legend(['Visit Rate', 'Average'], loc='best', fontsize='14')
    plt.tight_layout()
    # plt.show()
    print('Fig 03: Day wise visit rate generated')
    return plt.savefig('./Images/day_wise_visit_rate.png')
