# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 17:11:13 2021

@author: DECO
"""

import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

class Processor():
    
    def __init__(self, wallet, history):
        self.wallet = wallet
        self.history = history
        self.date1 = self.wallet.get_first_date()[:-2]+'01'
        
    def calculate_wallet_value(self, date1=None, date2=None):
        if date1 is None:
            date1 = self.date1
        if date2 is None:
            date2 = dt.datetime.now().strftime('%Y-%m-%d')
        dates = pd.bdate_range(date1, date2).strftime('%Y-%m-%d').to_list()
        value = []
        cost = []
        for date in dates:
            value.append(self.history.get_value_wallet(date, self.wallet))
            cost.append(self.wallet.get_cost(date))
        value = np.array(value)
        cost = np.array(cost)
        profit = (value-cost)/cost.clip(0.001, None)*100
        return value, cost, profit
