import matplotlib.pyplot as plt
import math
import numpy as np
import Functions.all_functions as fn

def day_wise_drop_size_value(drop_days,drop_size_val):
    ypos = np.arange(len(drop_days))

    avg = []
    for i in range(len(drop_size_val)):
        a = sum(drop_size_val) / len(drop_size_val)
        avg.append(a)

    fig, ax = plt.subplots(figsize=(12.81, 4.8))
    plt.ylim(0, math.ceil(max(drop_size_val) * 1.3))
    plt.plot(drop_size_val, color='#007cff', linewidth='3', marker='D', markerfacecolor="#fcff00")
    plt.plot(avg, color='#c3bdbd', linestyle='--', linewidth='2')

    # Show data point ---------------------------------------------------
    for i, v in enumerate(drop_size_val):
        ax.text(i, v + 10, fn.comma_seperator(v), ha="center", fontsize='14')

    ax.set_xticks(ypos)
    ax.set_xticklabels(drop_days, fontsize=14)

    plt.title('6. Day wise Drop Size Value', fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Days', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('Drop Size Value', fontsize='14', color='black', fontweight='bold')
    plt.legend(['Drop Size', 'Average'], loc='best', fontsize='14')
    plt.tight_layout()
    # plt.show()
    print('Fig 06: Day wise value drop size generated')
    return plt.savefig('./Images/day_wise_drop_size_val.png')
