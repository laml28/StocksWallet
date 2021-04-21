# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 23:14:29 2021

@author: DECO
"""

from classes.order import Order
from classes.stock import Stock
from classes.dividend import Dividend
from classes.fileio import FileIO

fileIO = FileIO()
wallet = fileIO.load_orders('database_orders.csv')

fileIO.update_stock_price_history(wallet.get_tickers(), 'brazil')
history = fileIO.load_stock_price_history(wallet.get_tickers())

value = history.get_value_wallet('2021-03-31', wallet)


#%%
import time
import pandas as pd
import matplotlib.pyplot as plt
t0 = time.time()
date_begin = wallet.get_first_date()[:-2]+'01'
dates = pd.bdate_range(date_begin, '2021-04-21').strftime('%Y-%m-%d').to_list()
value = []
for date in dates:
    value.append(history.get_value_wallet(date, wallet))
t = time.time()-t0

#%%
plt.plot(value)
rang = range(0, len(value), 50)
plt.xticks(rang, [dates[ii] for ii in rang], rotation=90)
plt.tight_layout()
