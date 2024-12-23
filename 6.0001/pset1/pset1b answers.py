# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 09:51:28 2022

@author: Joseph Mason
"""

# =============================================================================
# total_cost = float(int(input("What is the cost of your dream house?")))
# 
# portion_down_payment = 0.25 * total_cost
# 
# print("Given that the cost of your house is", total_cost, ", the down payment you will need to save is", portion_down_payment)
# 
# annual_salary = float(int(input("What is your current annual salary?")))
# 
# monthly_salary = float(annual_salary/12)
# 
# semi_annual_raise = float(int(input("What is your semi annual raise as a percentage?")))/100
# 
# portion_saved = float(input("What percentage of your monthly salary would you like to save each month?"))/100
# 
# current_savings = 0
# months = 0
# r = 0.04
# mr = 0.04/12
# cmr = 1+mr
# 
# while current_savings < portion_down_payment:
#     months += 1
#     if months % 6 == 0:
#         current_savings = current_savings*cmr
#         current_savings += portion_saved*monthly_salary
#         annual_salary = annual_salary*(1 + semi_annual_raise)
#         monthly_salary = float(annual_salary/12)
#         #Note: in this if statement it is important that the
#         # instructions are given in this order as the raise is
#         # semi-annual so you get the raise AFTER 6 months, not at 6 months.
#         # if the order of the lines in changed then the caluclation
#         # is incorrect by a small amount which affects large
#         # values
#     else:
#         current_savings = current_savings*cmr
#         current_savings += portion_saved*monthly_salary
# 
# print("It will take you", months, "months to save for this house.")
# =============================================================================


# Attempt no.2 using lecture 4 methods

# =============================================================================
# annual_salary = float(input("Enter your starting annual salary:"))
# portion_saved = float(input("Enter the percentage of your monthly salary you wish to save as a decimal:"))
# total_cost = float(input("Enter the cost of your dream home:"))
# semi_annual_raise = float(input("Enter your semi annual raise as a decimal:"))
# 
# def cur_sav_calc(x):
#     current_savings = 0
#     portion_down_payment = 0.25*total_cost
#     months = 0
#     r = 0.04
#     while current_savings < portion_down_payment:
#         months += 1
#         current_savings += (current_savings*r)/12
#         current_savings += x*(annual_salary/12)
#         if months % 6 == 0:
#             annual_salary = annual_salary*(1+semi_annual_raise)
#         else:
#             continue
#     return months
# 
# print("Number of months:", cur_sav_calc(portion_saved))
# =============================================================================
        
# Attempt 3 using lecture 4, emphasis on reusable code

annual_salary = float(input("Enter your starting salary:"))
portion_saved = float(input("Enter the percentage of your salary to save, as a decimal:"))
total_cost = float(input("Enter the cost of your dream home:"))
semi_annual_raise = float(input("Enter your semi-annual raise, as a decimal:"))

def cur_sav_calc2(x):
    """
    'x' should be the starting annual salary
    """
    current_savings = 0
    months = 0
    portion_down_payment = 0.25*total_cost
    r = 0.04
    while current_savings < portion_down_payment:
        months += 1
        current_savings += (current_savings*r)/12
        current_savings += (x/12)*(portion_saved)
        if months % 6 == 0:
            x = x*(1 + semi_annual_raise)
        else:
            x = x
    return months
                            
print("Number of months:", cur_sav_calc2(annual_salary))
                            
"""
This is the most efficient way of solving problem B
and it will allow code to be reused for part c.
All the examples are correct as well.
There may still be an alternative where the portion saved 
is used as an input into the function
"""
                            
        
                            
        
                            