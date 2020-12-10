import matplotlib.pyplot as plt
import math
import Functions.all_functions as fn
import numpy as np


def day_wise_lpc_rate(lpc_days, lpc_rate):
    range(1, len(lpc_days) + 1, 1)
    ypos = np.arange(len(lpc_days))

    avg = []
    for i in range(len(lpc_rate)):
        a = sum(lpc_rate) / len(lpc_rate)
        avg.append(a)

    fig, ax = plt.subplots(figsize=(12.81, 4.8))
    plt.ylim(0, max(lpc_rate) + 2, 1)
    plt.plot(lpc_rate, color='#007cff', linewidth='3', marker='D', markerfacecolor="#fcff00")
    plt.plot(avg, color='#c3bdbd', linestyle='--', linewidth='2')
    # Show data point ----------------------------------------

    for i, v in enumerate(lpc_rate):
        ax.text(i, v + .1, "%d" % v, ha="center", fontsize='14')

    ax.set_xticks(ypos)
    ax.set_xticklabels(lpc_days, fontsize=14)

    plt.title('05. Day wise LPC Rate', fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Days', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('LPC Rate', fontsize='14', color='black', fontweight='bold')
    plt.legend(['LPC Rate', 'Average'], loc='best', fontsize='14')
    plt.tight_layout()
    # plt.show()
    print('Fig 05: Day wise LPC Rate generated')
    return plt.savefig('./Images/day_wise_lpc_rate.png')
