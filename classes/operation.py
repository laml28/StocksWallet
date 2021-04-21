# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 23:14:29 2021

@author: DECO
"""

import numpy as np

class Operation():
    
    def __init__(self, date=None, amount=0, cost=0, kind='buy'):
        self.date = date
        self.amount = amount
        self.cost = cost
        self.kind = kind
        
    def __repr__(self):
        return 'Operation({}, {}, {}, \'{}\')'.format(self.date, self.amount,
                                                  self.cost, self.kind)
    
    def __str__(self):
        if self.kind == 'split':
            return '{}: split yields {} stocks'.format(self.date, self.amount)
        else:
            return '{}: {} {} stocks at ${}'.format(self.date, self.kind, 
                                                    self.amount, self.cost)
    
    def __add__(self, other):
        # If it's a sell operation, the amount becomes negative
        amount_a = self.amount*(2*(self.kind != 'sell')-1) 
        amount_b = other.amount*(2*(other.kind != 'sell')-1)
        amount = amount_a + amount_b
        # If both are of the same kind, the cost is the weighted average
        if np.sign(amount_a)*np.sign(amount_b) >= 0:
            cost = (((self.amount*self.cost) + (other.amount*other.cost))
                    /(self.amount + other.amount))
        # If one is a buy and the other is a sell, the cost stays the same
        else:
            cost = self.cost
        # If the final amount remaining is positive, it's classified as buy
        if amount > 0:
            kind = 'buy'
        else:
            kind = 'sell'
        return Operation(None, amount, cost, kind)