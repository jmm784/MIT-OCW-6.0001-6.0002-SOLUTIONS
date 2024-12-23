# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 20:30:27 2022

@author: Joseph Mason
"""
print("Hello! This programme will calculate how many months it will take you to save up for a down payment on a house. Please follow the instructions:")
total_cost = float(int(input("What is the cost of your dream house?")))
portion_down_payment = 0.25 * total_cost
print("Given that the cost of your house is", total_cost, ", the down payment you will need to save is", portion_down_payment)
annual_salary = float(int(input("What is your current annual salary?")))
monthly_salary = float(annual_salary/12)
print("Your monthly salary is", monthly_salary)
portion_saved = float(input("What percentage of your monthly salary would you like to save each month?"))/100
#Note: The above line is written so that the user can
# give the amount they want to save each month as a percentage instead
# of a decimal as I think this will reduce input errors. As can be seen,
# to convert from a percentage to a decimal the percentage is divided by 100

current_savings = 0
months = 0
r = 0.04
#Note: r is the annual return on investment
mr = 0.04/12
#Note: mr is the monthly return on investment
cmr = 1+mr
#Note: cmr is the amount I will multiply the current_savings by eaach month to get an
# interest-adjusted savings amount

while current_savings < portion_down_payment:
    months += 1
    current_savings = current_savings*cmr
    current_savings += portion_saved*monthly_salary
    #Note: in the above line this is the amount being added to the savings each month
    # from your salary
    #Note: the current savings are only multiplied by the interest rates after one month
    # as there is a one month delay in the time it takes for your ROI to be added to the
    # current savings account (profits from investments are not instantaneous)

print("It will take you", months, "months to save for this house.")
    

