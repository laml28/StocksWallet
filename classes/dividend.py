# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 23:44:05 2021

@author: DECO
"""

class Dividend():
    
    def __init__(self, date=None, value=0):
        self.date = date
        self.value = 0
        
    def __repr__(self):
        return 'Dividend({}, {})'.format(self.date, self.value)
    
    def __str__(self):
        return '{}: received dividends worth ${}'.format(self.date, self.value)
    
    def __add__(self, other):
        return Dividend(None, self.value+other.value)