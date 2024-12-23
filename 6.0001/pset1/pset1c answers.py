# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 15:31:42 2022

@author: Joseph Mason
"""

#Standard variables
# =============================================================================
# starting_salary = float(int(input("Enter your starting salary:")))
# annual_salary = starting_salary
# total_cost = 1000000
# portion_down_payment = 0.25*total_cost
# monthly_salary = annual_salary/12
# semi_annual_raise = 0.07
# r = 0.04
# mr = 0.04/12
# cmr = 1 + mr
# months = 0
# current_savings = 0
# 
# #Bisection search
# low = 0
# high = 1000
# epsilon = 100
# guess = (high + low)/2
# num_guess = 0
# 
# while abs(current_savings - portion_down_payment) > epsilon:
#     current_savings = 0
#     annual_salary = starting_salary
#     monthly_salary = annual_salary/12
#     for months in range(1, 36):
#         if months % 6 == 0:
#             current_savings = current_savings*cmr
#             current_savings += (guess/1000)*monthly_salary
#             annual_salary = annual_salary*(1 + semi_annual_raise)
#             monthly_salary = annual_salary/12
#         else:
#             current_savings = current_savings*cmr
#             current_savings += (guess/1000)*monthly_salary
#     if current_savings < portion_down_payment:
#         low = guess
#     else:
#         high = guess
#     guess = (high + low)/2
#     num_guess += 1
#             
# print(guess/1000)
# print(num_guess)           
# =============================================================================
            
#Attempt 2 with emphasis on reusable code from part B

annual_salary = float(input("Enter your starting salary:"))
semi_annual_raise = 0.07
total_cost = 1000000
portion_down_payment = 0.25*total_cost

low = 0
high = 1000
epsilon = 100
guess = (high + low)/2
num_guess = 0


#Reusable section
def cur_sav_calc2(x):
    """
    'x' should be the starting annual salary
    """
    current_savings = 0
    months = 0
    r = 0.04
    for months in range(1, 36):
        current_savings += (current_savings*r)/12
        current_savings += (x/12)*(guess/1000)
        if months % 6 == 0:
            x += x*semi_annual_raise
        else:
            x = x
    return current_savings

guess = 1000
if cur_sav_calc2(annual_salary) < portion_down_payment:
    print("It is not possible to pay the down payment in 3 years")

low = 0
high = 1000
epsilon = 100
guess = (high + low)/2
num_guess = 0

while abs((cur_sav_calc2(annual_salary) - portion_down_payment)) > epsilon:
    if cur_sav_calc2(annual_salary) < portion_down_payment:
        low = guess
    else:
        high = guess
    guess = (high + low)/2
    num_guess += 1

print("Best savings rate:", guess/1000)
print("Steps in Bisection search:", num_guess)
print(cur_sav_calc2(annual_salary))

# Note: the answers given by this piece of code are not the same as the answers
# in the examples. This is not a problem as they said there are multiple
# ways to code this that give different answers in the same proximity

# Note: check tomorrow how to get final rate to 2DP

    
            
            
            
            
            
            
            