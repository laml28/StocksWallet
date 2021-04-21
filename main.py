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
wallet = fileIO.load_orders('database_orders.csv')

fileIO.update_stock_price_history(wallet.get_tickers(), 'brazil')
history = fileIO.load_stock_price_history(wallet.get_tickers())

value = history.get_value_wallet('2021-03-31', wallet)

processor = Processor(wallet, history)

a,b,c = processor.calculate_wallet_value()