import numpy as np
import matplotlib.pyplot as plt


def day_wise_strike_rate(strike_days, day_strike_rate):
    range(1, len(strike_days) + 1, 1)
    ypos = np.arange(len(strike_days))
    # range(len(d.strike_days1))
    avg = []
    for i in range(len(day_strike_rate)):
        a = sum(day_strike_rate) / len(day_strike_rate)
        avg.append(a)

    fig, ax = plt.subplots(figsize=(12.81, 4.8))
    plt.ylim(0, 101, 10)
    plt.plot(day_strike_rate, color='#007cff', linewidth='3', marker='D', markerfacecolor="#fcff00")
    plt.plot(avg, color='#c3bdbd', linestyle='--', linewidth='2')

    # Show data point ----------------------------------------
    for i, v in enumerate(day_strike_rate):
        ax.text(i, v + 3, str(v) + '%', ha="center", fontsize='14')

    ax.set_xticks(ypos)
    ax.set_xticklabels(strike_days, fontsize=14)

    plt.title('04. Day wise Strike Rate', fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Days', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('Strike Rate %', fontsize='14', color='black', fontweight='bold')
    plt.legend(['Strike Rate', 'Average'], loc='best', fontsize='14')
    plt.tight_layout()
    # plt.show()
    print('Fig 04: Day wise strike rate generated')
    return plt.savefig('./Images/day_wise_strike_rate.png')
