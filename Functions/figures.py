import matplotlib.pyplot as plt
import numpy as np
import Functions.kpi as d
import math


def thousand_converter(number):
    number = int(number / 1000)
    number = format(number, ',')
    number = number + 'K'
    return number


def comma_seperator(number):
    number = format(int(number), ',')
    return number


# # # -------- Day wise strike Rate line chart ----------------------
def day_wise_strike_rate():
    range(1, len(d.strike_days1) + 1, 1)
    ypos = np.arange(len(d.strike_days1))
    # range(len(d.strike_days1))
    avg = []
    for i in range(len(d.day_strike_rate)):
        a = sum(d.day_strike_rate) / len(d.day_strike_rate)
        avg.append(a)

    fig, ax = plt.subplots(figsize=(12.81, 4.8))
    plt.ylim(0, 101, 10)
    plt.plot(d.day_strike_rate, color='#007cff', linewidth='3', marker='D', markerfacecolor="#fcff00")
    plt.plot(avg, color='#c3bdbd', linestyle='--', linewidth='2')

    # Show data point ----------------------------------------
    for i, v in enumerate(d.day_strike_rate):
        ax.text(i, v + 3, str(v) + '%', ha="center", fontsize='14')

    ax.set_xticks(ypos)
    ax.set_xticklabels(d.strike_days1, fontsize=14)

    plt.title('04. Day wise Strike Rate', fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Days', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('Strike Rate %', fontsize='14', color='black', fontweight='bold')
    plt.legend(['Strike Rate', 'Average'], loc='best', fontsize='14')
    plt.tight_layout()
    # plt.show()
    print('Fig 04: Day wise strike rate generated')
    return plt.savefig('./Images/day_wise_strike_rate.png')


# # # -------- Day wise visit Rate ----------------------------------
def day_wise_visit_rate():
    range(1, len(d.visit_days) + 1, 1)
    ypos = np.arange(len(d.visit_days))

    avg = []
    for i in range(len(d.day_visit_rate)):
        a = sum(d.day_visit_rate) / len(d.day_visit_rate)
        avg.append(a)

    fig, ax = plt.subplots(figsize=(12.81, 4.8))
    plt.ylim(0, 101, 10)
    plt.plot(d.day_visit_rate, color='#007cff', linewidth='3', marker='D', markerfacecolor="#fcff00")
    plt.plot(avg, color='#c3bdbd', linestyle='--', linewidth='2')

    # Show data point ----------------------------------------------
    for i, v in enumerate(d.day_visit_rate):
        ax.text(i, v + 3, str(v) + '%', ha="center", fontsize='14')

    ax.set_xticks(ypos)
    ax.set_xticklabels(d.visit_days, fontsize=14)

    plt.title('03. Day wise Visit Rate', fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Days', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('Visit Rate %', fontsize='14', color='black', fontweight='bold')
    plt.legend(['Visit Rate', 'Average'], loc='best', fontsize='14')
    plt.tight_layout()
    # plt.show()
    print('Fig 03: Day wise visit rate generated')
    return plt.savefig('./Images/day_wise_visit_rate.png')


# # -------- Day wise LPC Rate --------------------------------------
def day_wise_lpc_rate():
    range(1, len(d.lpc_days) + 1, 1)
    ypos = np.arange(len(d.lpc_days))

    avg = []
    for i in range(len(d.lpc_rate)):
        a = sum(d.lpc_rate) / len(d.lpc_rate)
        avg.append(a)

    fig, ax = plt.subplots(figsize=(12.81, 4.8))
    plt.ylim(0, max(d.lpc_rate) + 2, 1)
    plt.plot(d.lpc_rate, color='#007cff', linewidth='3', marker='D', markerfacecolor="#fcff00")
    plt.plot(avg, color='#c3bdbd', linestyle='--', linewidth='2')
    # Show data point ----------------------------------------
    for i, v in enumerate(d.lpc_rate):
        ax.text(i, v + .1, "%d" % v, ha="center", fontsize='14')

    ax.set_xticks(ypos)
    ax.set_xticklabels(d.lpc_days, fontsize=14)

    plt.title('05. Day wise LPC Rate', fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Days', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('LPC Rate', fontsize='14', color='black', fontweight='bold')
    plt.legend(['LPC Rate', 'Average'], loc='best', fontsize='14')
    plt.tight_layout()
    # plt.show()
    print('Fig 05: Day wise LPC Rate generated')
    return plt.savefig('./Images/day_wise_lpc_rate.png')


# # ------ Day wise Drop Size Value ---------------------------------
def day_wise_drop_size_value():
    ypos = np.arange(len(d.drop_days))

    avg = []
    for i in range(len(d.drop_size_val)):
        a = sum(d.drop_size_val) / len(d.drop_size_val)
        avg.append(a)

    fig, ax = plt.subplots(figsize=(12.81, 4.8))
    plt.ylim(0, math.ceil(max(d.drop_size_val) * 1.3))
    plt.plot(d.drop_size_val, color='#007cff', linewidth='3', marker='D', markerfacecolor="#fcff00")
    plt.plot(avg, color='#c3bdbd', linestyle='--', linewidth='2')

    # Show data point ---------------------------------------------------
    for i, v in enumerate(d.drop_size_val):
        ax.text(i, v + 10, comma_seperator(v), ha="center", fontsize='14')

    ax.set_xticks(ypos)
    ax.set_xticklabels(d.drop_days, fontsize=14)

    plt.title('6. Day wise Drop Size Value', fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Days', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('Drop Size Value', fontsize='14', color='black', fontweight='bold')
    plt.legend(['Drop Size', 'Average'], loc='best', fontsize='14')
    plt.tight_layout()
    # plt.show()
    print('Fig 06: Day wise value drop size generated')
    return plt.savefig('./Images/day_wise_drop_size_val.png')


# # ----------- Day wise Drop Size Kg -------------------------------
def day_wise_drop_size_kg():
    range(1, len(d.drop_days) + 1, 1)
    ypos = np.arange(len(d.drop_days))
    range(len(d.drop_size_kg))

    fig, ax = plt.subplots(figsize=(12.81, 4.8))
    plt.ylim(0, math.ceil(max(d.drop_size_kg) * 1.2))
    plt.plot(d.drop_size_kg, color='#b100ff', linewidth='3', marker='D', markerfacecolor="red")

    # Show data point ----------------------------------------
    for i, v in enumerate(d.drop_size_kg):
        ax.text(i, v + .1, str(round(v, 2)) + 'Kg', ha="center", fontsize='14', rotation=10)

    ax.set_xticks(ypos)
    ax.set_xticklabels(d.drop_days, fontsize=14)

    plt.title('7. Day wise Drop Size in Kg', fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Days', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('Drop Size Kg', fontsize='14', color='black', fontweight='bold')
    plt.legend(['Drop Size Kg'], loc='upper right', fontsize='14')
    plt.tight_layout()
    # plt.show()
    print('Fig 07: Drop size kg generated')
    return plt.savefig('./Images/day_wise_drop_size_kg.png')


def sales_kg_chart():
    brand_list = d.brand_list
    sales_kg_list = d.sales_kg_list
    fig, ax = plt.subplots(figsize=(6.4, 4.8))

    colors = ['yellow', 'orange', 'violet', '#DADADA', '#003f5c', '#665191', '#a05195', '#d45087', '#ff7c43', '#ffa600']
    bars = plt.bar(brand_list, height=sales_kg_list, color='#1ecc00', width=.70)
    plt.plot(d.branch_mtd_target_kg_list, color='#007cff', linewidth='3', marker='D', markerfacecolor="red")

    def autolabel(bars):
        for bar in bars:
            height = int(bar.get_height())
            ax.text(bar.get_x() + bar.get_width() / 2., .995 * height, str(height) + 'Kg',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

    autolabel(bars)

    for i, v in enumerate(d.branch_mtd_target_kg_list):
        ax.text(i, v, str(comma_seperator(v)) + 'Kg', ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.ylim(0, math.ceil(max(d.branch_mtd_target_kg_list) * 1.2))
    plt.title("02. Brand wise Sales in KG", fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Brand', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('Sales Kg', fontsize='14', color='black', fontweight='bold')

    plt.rcParams['text.color'] = 'black'
    plt.legend(['Target', 'Sales'], loc='best', fontsize='14')

    plt.tight_layout()
    # plt.show()
    print('Fig 02: Brand wise sales in kg generated')
    return plt.savefig('./Images/brand_wise_sales_kg.png')


def sales_val_chart(brand_list, ):

    sales_val_list = d.Sales_Val_list
    fig, ax = plt.subplots(figsize=(6.4, 4.8))

    colors = ['yellow', 'orange', 'violet', '#DADADA', '#003f5c', '#665191', '#a05195', '#d45087', '#ff7c43', '#ffa600']
    bars = plt.bar(brand_list, height=sales_val_list, color='#1ecc00', width=.70)
    plt.plot(d.branch_mtd_target_list, color='#007cff', linewidth='3', marker='D', markerfacecolor="red")
    plt.ylim(0, math.ceil(max(d.branch_mtd_target_list) * 1.2))

    def autolabel(bars):
        for bar in bars:
            height = int(bar.get_height())
            ax.text(bar.get_x() + bar.get_width() / 2., .995 * height, thousand_converter(height),
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

    autolabel(bars)

    for i, v in enumerate(d.branch_mtd_target_list):
        ax.text(i, v, thousand_converter(v), ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.title("01. Brand wise Sales in Value ", fontsize=16, fontweight='bold', color='#3e0a75')
    plt.xlabel('Brand', fontsize='14', color='black', fontweight='bold')
    plt.ylabel('Values', fontsize='14', color='black', fontweight='bold')
    plt.legend(['Target', 'Sales'], loc='best', fontsize='14')

    plt.rcParams['text.color'] = 'black'
    plt.tight_layout()
    # plt.show()
    print('Fig 01: Brand wise sales in Value generated')
    return plt.savefig('./Images/brand_wise_sales_val.png')
