# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 00:56:45 2021

@author: DECO
"""

import pandas as pd
from classes.stock import Stock
from classes.order import Order
from classes.wallet import Wallet

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