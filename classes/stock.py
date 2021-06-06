# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 23:46:15 2021

@author: DECO
"""

from classes.order import Order
from classes.dividend import Dividend

class Stock():
    
    def __init__(self, ticker='ABCD', list_orders=[], 
                 list_dividends=[], amount=0, cost=0):
        self.ticker = ticker
        self.list_orders = list_orders
        self.list_dividends = list_dividends
        self.amount = amount
        self.cost = cost
        if self.amount == 0:
             self.update_amount()
        
    def __repr__(self):
        return 'Stock({}, {}, {}, {}, {})'.format(self.ticker,
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
            cost = op_sum.price*amount
        else:
            amount = 0
            cost = 0.0
        return amount, cost
    
    def get_dividends(self, date):
        divs_before = [div for div in self.list_dividends if div.date <= date]
        if len(divs_before) > 0:
            div_sum = sum(divs_before, Dividend())
            value = div_sum.value
        else:
            value = 0.0
        return value
    
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
        self.cost = op_sum.price*self.amount
        
    def get_first_date(self):
        date_start = min([order.date for order in self.list_orders])
        return date_start