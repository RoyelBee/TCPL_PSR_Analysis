import matplotlib.pyplot as plt
import math
import Functions.all_functions as fn
import numpy as np

def day_wise_drop_size_kg(drop_days, drop_size_kg):
    range(1, len(drop_days) + 1, 1)
    ypos = np.arange(len(drop_days))
    range(len(drop_size_kg))

    fig, ax = plt.subplots(figsize=(12.81, 4.8))
    plt.ylim(0, math.ceil(max(drop_size_kg) * 1.2))
    plt.plot(drop_size_kg, color='#b100ff', linewidth='3', marker='D', markerfacecolor="red")

    # Show data point ----------------------------------------
    for i, v in enumerate(drop_size_kg):
        ax.text(i, v + .1, str(round(v, 2)) + 'Kg', ha="center", fontsize='14', rotation=10)

    ax.set_xticks(ypos)
    ax.set_xticklabels(drop_days, fontsize=14)

    plt.title('7. Day wise Drop Size in Kg', fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Days', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('Drop Size Kg', fontsize='14', color='black', fontweight='bold')
    plt.legend(['Drop Size Kg'], loc='upper right', fontsize='14')
    plt.tight_layout()
    # plt.show()
    print('Fig 07: Drop size kg generated')
    return plt.savefig('./Images/day_wise_drop_size_kg.png')
