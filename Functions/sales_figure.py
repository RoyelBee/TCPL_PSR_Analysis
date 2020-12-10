import matplotlib.pyplot as plt
import math
import Functions.all_functions as fn

def sales_val_chart(brand_list, Sales_Val_list, branch_mtd_target_list):
    fig, ax = plt.subplots(figsize=(6.4, 4.8))

    colors = ['yellow', 'orange', 'violet', '#DADADA', '#003f5c', '#665191', '#a05195', '#d45087', '#ff7c43', '#ffa600']
    bars = plt.bar(brand_list, height=Sales_Val_list, color='#1ecc00', width=.70)
    plt.plot(branch_mtd_target_list, color='#007cff', linewidth='3', marker='D', markerfacecolor="red")
    plt.ylim(0, math.ceil(max(branch_mtd_target_list) * 1.2))

    def autolabel(bars):
        for bar in bars:
            height = int(bar.get_height())
            ax.text(bar.get_x() + bar.get_width() / 2., .995 * height, fn.thousand_converter(height),
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

    autolabel(bars)

    for i, v in enumerate(branch_mtd_target_list):
        ax.text(i, v, fn.thousand_converter(v), ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.title("01. Brand wise Sales in Value ", fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Brand', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('Values', fontsize='14', color='black', fontweight='bold')
    plt.legend(['Target', 'Sales'], loc='best', fontsize='14')

    plt.rcParams['text.color'] = 'black'
    plt.tight_layout()
    # plt.show()
    print('Fig 01: Brand wise sales in Value generated')
    return plt.savefig('./Images/brand_wise_sales_val.png')
