# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 23:14:29 2021

@author: DECO
"""

from classes.order import Order
from classes.stock import Stock
from classes.dividend import Dividend
from classes.fileio import FileIO

op1 = Order('2020-01-01', 10, 5, 'buy')
op2 = Order('2020-02-01', 10, 7, 'buy')
op3 = Order('2020-03-01', 15, 10, 'sell')

div1 = Dividend(None, 10)
div2 = Dividend(None, 15)

stock = Stock('WEGE3', [op1, op2, op3], [div1, div2])
stock2 = Stock('WEGE3')
stock2.add_order(op1)
stock2.add_order([op2, op3])
stock2.add_dividend(div1)
stock2.add_dividend([div2])

fileIO = FileIO()
wallet = fileIO.load_orders('database.txt')

fileIO.update_stock_price_history([stock.ticker for stock in 
                                   wallet.list_stocks])
history = fileIO.load_stock_price_history([stock.ticker for stock in 
                                   wallet.list_stocks])

value = history.get_value_wallet('2020-01-03', wallet)