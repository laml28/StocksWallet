# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 23:46:15 2021

@author: DECO
"""

from classes.order import Order

class Stock():
    
    def __init__(self, name=None, ticker='ABCD', list_orders=[], 
                 list_dividends=[], amount=0, cost=0):
        self.name = name
        self.ticker = ticker
        self.list_orders = list_orders
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
        orders_before = [op for op in self.list_orders if op.date <= date]
        if len(orders_before) > 0:
            op_sum = sum(orders_before, Order())
            amount = op_sum.amount
            cost = op_sum.cost
        else:
            amount = 0
            cost = 0
        return amount, cost
    
    def add_order(self, order):
        if isinstance(order, list):
            self.list_orders = self.list_orders + order
        else:
            self.list_orders.append(order)
        self.update_amount()
        
    def add_dividend(self, dividend):
        if isinstance(dividend, list):
            self.list_dividends = self.list_dividends + dividend
        else:
            self.list_dividends.append(dividend)
            
    def update_amount(self):
        op_sum = sum(self.list_orders, Order())
        self.amount = op_sum.amount
        self.cost = op_sum.cost