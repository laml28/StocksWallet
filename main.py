# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 23:14:29 2021

@author: DECO
"""

from classes.order import Order
from classes.stock import Stock
from classes.dividend import Dividend
from classes.fileio import FileIO
from classes.processor import Processor

import matplotlib.pyplot as plt

fileIO = FileIO()
wallet = fileIO.load_orders('database_orders.csv', 'database_dividends.csv')

fileIO.update_stock_price_history(wallet.get_tickers(), 'brazil')
history = fileIO.load_stock_price_history(wallet.get_tickers())

value = history.get_value_wallet('2021-03-31', wallet)

processor = Processor(wallet, history)

wallet_timeseries = processor.calculate_wallet_value()

df = processor.table_results('2021-04-01')
processor.plot_results()

#%%
# plt.figure()
# plt.plot(wallet_timeseries['Value'])
# plt.ylabel('Wallet Total (R$)')
# plt.grid()

# plt.figure()
# plt.plot(wallet_timeseries['Profit'])
# plt.ylabel('Total Profit (%)')
# plt.grid()