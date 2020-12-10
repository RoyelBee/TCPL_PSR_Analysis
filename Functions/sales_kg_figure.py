import matplotlib.pyplot as plt
import math
import Functions.all_functions as fn


def sales_kg_chart(brand_list, sales_kg_list, branch_mtd_target_kg_list):

    fig, ax = plt.subplots(figsize=(6.4, 4.8))

    colors = ['yellow', 'orange', 'violet', '#DADADA', '#003f5c', '#665191', '#a05195', '#d45087', '#ff7c43', '#ffa600']
    bars = plt.bar(brand_list, height=sales_kg_list, color='#1ecc00', width=.70)
    plt.plot(branch_mtd_target_kg_list, color='#007cff', linewidth='3', marker='D', markerfacecolor="red")

    def autolabel(bars):
        for bar in bars:
            height = int(bar.get_height())
            ax.text(bar.get_x() + bar.get_width() / 2., .995 * height, str(height) + 'Kg',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

    autolabel(bars)

    for i, v in enumerate(branch_mtd_target_kg_list):
        ax.text(i, v, str(fn.comma_seperator(v)) + 'Kg', ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.ylim(0, math.ceil(max(branch_mtd_target_kg_list) * 1.2))
    plt.title("02. Brand wise Sales in KG", fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Brand', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('Sales Kg', fontsize='14', color='black', fontweight='bold')

    plt.rcParams['text.color'] = 'black'
    plt.legend(['Target', 'Sales'], loc='best', fontsize='14')

    plt.tight_layout()
    # plt.show()
    print('Fig 02: Brand wise sales in kg generated')
    return plt.savefig('./Images/brand_wise_sales_kg.png')

