# import Functions.targets as trg
#
# trg_val = trg.TotalTarget(22)[0]
# trg_kh = trg.TotalTarget(22)[1]
#
# import Functions.returns as re
#
# return_val = re.TotalReturn(22)[0]
# return_kg = re.TotalReturn(22)[1]

import Functions.user_profiles as up

sr_name = up.UserProfile(22)[0]
reporting_boss = up.UserProfile(22)[1]
total_brand = up.UserProfile(22)[2]
designation = up.UserProfile(22)[3]
sales_val = up.UserProfile(22)[4]
sales_kg = up.UserProfile(22)[5]
brand_list = up.UserProfile(22)[6]
target_list = up.UserProfile(22)[7]
target_kg_list = up.UserProfile(22)[8]

print(sales_val)

# import Functions.visit_rates as vr
#
# visit_days = vr.VisitRate(22)[0]
# SalesCustomer = vr.VisitRate(22)[1]
# VisitedCustomer = vr.VisitRate(22)[2]
#
# import Functions.customers as vc
#
# total_cust = vc.TotalCust(22)
# effective_cust = vc.EffectiveCust(22)
# visited_cust = vc.VisitCust(22)
#
# import Functions.strike_days as strike
#
# strike_days = strike.StrikeDays(22)[0]
# effective_strike = strike.StrikeDays(22)[1]
# totalCustomer_strike = strike.StrikeDays(22)[2]
#
# sr = ((effective_strike / totalCustomer_strike) * 100).tolist()
# day_strike_rate = []
# for i in range(len(sr)):
#     day_strike_rate.append(int(sr[i]))
#
# import Functions.lpcs as lpc
#
# lpc_days = lpc.DayWiseLPC(22)[0]
# lpc_rate = lpc.DayWiseLPC(22)[1]
#
# import Functions.drop_size as ds
#
# drop_days = ds.DayWiseDropSize(22)[0]
# drop_size_val = ds.DayWiseDropSize(22)[1]
# drop_size_kg = ds.DayWiseDropSize(22)[2]
#
