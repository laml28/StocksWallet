# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 00:56:45 2021

@author: DECO
"""

import pandas as pd
from classes.stock import Stock
from classes.order import Order
from classes.wallet import Wallet
from classes.history import History

class FileIO():
    
    def load_orders(self, path):
        orders = pd.read_csv(path, sep=';', index_col=0, header=0)
        list_stocks = []
        for ticker in orders.index.unique():
            list_orders = []
            for row in orders.loc[ticker].iterrows():
                list_orders.append(Order(row[1]['Date'], row[1]['Amount'],
                                         row[1]['Price'], row[1]['Kind']))
            list_stocks.append(Stock(ticker, list_orders))
        return Wallet(list_stocks)
    
    def update_stock_price_history(self, tickers):
        for ticker in tickers:
            df = pd.DataFrame(columns=['Price'])
            df.loc['2020-01-01'] = [10]
            df.loc['2020-01-02'] = [11]
            df.loc['2020-01-03'] = [12]
            df.loc['2020-01-04'] = [13]
            df.loc['2020-01-05'] = [14]
            df = df.reset_index()
            df.columns = ['Date', 'Price']
            df.to_csv('price_history\\{}.txt'.format(ticker), index=False, 
                      header=True, sep=';')
        
    def load_stock_price_history(self, tickers):
        history = History()
        for ticker in tickers:
            data = pd.read_csv('price_history\\{}.txt'.format(ticker), 
                               index_col=0, header=0, sep=';')
            history.add_data(ticker, data)
        return history
            