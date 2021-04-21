# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 01:04:47 2021

@author: DECO
"""

class Wallet():
    
    def __init__(self, list_stocks=[]):
        self.list_stocks = list_stocks
    
    def add_stock(self, stock):
        if isinstance(stock, list):
            self.list_stocks = self.list_stocks + stock
        else:
            self.list_stocks.append(stock)
        self.update_amount()
        
    def __repr__(self):
        return 'Wallet([])'
    
    def __str__(self):
        mystr = 'Wallet contains:'
        for stock in self.list_stocks:
            mystr += ' {} {},'.format(stock.amount, stock.ticker)
        return mystr[:-1]
    
    def get_cost(self, date):
        return sum([stock.get_amount_cost(date)[1] for stock in self.list_stocks])