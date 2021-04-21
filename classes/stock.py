# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 23:46:15 2021

@author: DECO
"""

from classes.operation import Operation

class Stock():
    
    def __init__(self, name=None, ticker='ABCD', list_operations=[], 
                 list_dividends=[], amount=0, cost=0):
        self.name = name
        self.ticker = ticker
        self.list_operations = list_operations
        self.list_dividends = list_dividends
        self.amount = amount
        self.cost = cost
        if self.amount == 0:
             self.update_amount()
        
    def __repr__(self):
        return 'Stock({}, {}, {}, {}, {}, {})'.format(self.name,
                                                      self.ticker,
                                                      [],
                                                      [],
                                                      self.amount,
                                                      self.cost)
    
    def __str__(self):
        return '{}: {} stocks with a total cost of ${}'.format(self.ticker,
                                                               self.amount,
                                                               self.cost)
    
    def get_amount_cost(self, date):
        operations_before = [op for op in self.list_operations if op.date <= date]
        if len(operations_before) > 0:
            op_sum = sum(operations_before, Operation())
            amount = op_sum.amount
            cost = op_sum.cost
        else:
            amount = 0
            cost = 0
        return amount, cost
    
    def add_operation(self, operation):
        if isinstance(operation, list):
            self.list_operations = self.list_operations + operation
        else:
            self.list_operations.append(operation)
        self.update_amount()
        
    def add_dividend(self, dividend):
        if isinstance(dividend, list):
            self.list_dividends = self.list_dividends + dividend
        else:
            self.list_dividends.append(dividend)
            
    def update_amount(self):
        op_sum = sum(self.list_operations, Operation())
        self.amount = op_sum.amount
        self.cost = op_sum.cost