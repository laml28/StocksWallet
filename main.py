# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 23:14:29 2021

@author: DECO
"""

from classes.order import Order
from classes.stock import Stock
from classes.dividend import Dividend

op1 = Order('2020-01-01', 10, 5, 'buy')
op2 = Order('2020-02-01', 10, 7, 'buy')
op3 = Order('2020-03-01', 15, 10, 'sell')

div1 = Dividend(None, 10)
div2 = Dividend(None, 15)

stock = Stock('MyCompany', 'MCMP', [op1, op2, op3], [div1, div2])
stock2 = Stock('MyCompany', 'MCMP')
stock2.add_order(op1)
stock2.add_order([op2, op3])
stock2.add_dividend(div1)
stock2.add_dividend([div2])

