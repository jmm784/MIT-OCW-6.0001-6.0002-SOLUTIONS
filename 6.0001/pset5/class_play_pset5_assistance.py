# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 21:04:21 2022

@author: Joseph Mason
"""

# =============================================================================
# class MyClass:
#     i = 12345
#     
#     def f(self):
#         return 'Hello World'
# 
# print(MyClass.i)
# x = MyClass()
# print(x.f())
# 
# H = "HELLO"
# print(H.lower())
# =============================================================================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError
        
class PhraseTrigger(Trigger):
    def __init__(self, string_phrase):
        self.string_phrase = string_phrase.lower()
        
    def is_phrase_in(self, self.string_phrase):
        if self.string_phrase in self.evaluate(story):
            return True
        
test1 = PhraseTrigger("Hello world")
print(test1.is_phrase_in())


























