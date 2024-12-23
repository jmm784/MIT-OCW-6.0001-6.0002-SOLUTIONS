# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 21:22:32 2024

@author: josep
"""
dict_test = {'Betty': 9, 'Smelly': 11, 'Daniel': 4}
print(dict_test)
dict_test = dict(sorted(dict_test.items(), key=lambda item:item[1]))
print(dict_test)
print(dict_test[0])