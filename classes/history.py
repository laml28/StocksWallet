# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 01:26:46 2021

@author: DECO
"""

class History():
    
    def __init__(self, data={}):
        self.data = data
        
    def __repr__(self):
        return 'History([])'
    
    def __str__(self):
        return ('History for' + [' {},'.format(tkr) for tkr in 
                                  self.data])[:-1]
    
    def add_data(self, ticker, data):
        self.data[ticker] = data
        
    def get_value_stock(self, date, ticker):
        return self.data[ticker].loc[self.data[ticker].index<=date].iloc[-1,0]
    
    def get_value_wallet(self, date, wallet):
        value = 0
        for stock in wallet.list_stocks:
            value += (stock.get_amount_cost(date)[0]
                      *self.get_value_stock(date, stock.ticker))
        return value