# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 23:14:29 2021

@author: DECO
"""

from classes.fileio import FileIO
from classes.processor import Processor
from classes.history import History

# Read the database files and create the Wallet with all that information
fileIO = FileIO()
wallet_BR = fileIO.load_orders('database_orders_BR.csv',
                                'database_dividends_BR.csv',
                                'brazil')
wallet_US = fileIO.load_orders('database_orders_US.csv',
                               'database_dividends_US.csv',
                               'united states')

# Update the database for stock prices
fileIO.update_stocks_price_history(wallet_BR.get_tickers(), 'brazil')
fileIO.update_stocks_price_history(wallet_US.get_tickers(), 'united states')
fileIO.update_stock_price_history('BVSP', 'brazil')
fileIO.update_ipca_history()
fileIO.update_dollar_history()

# Load the stocks price history
history = History()
fileIO.load_stock_price_history(wallet_BR.get_tickers(), history)
fileIO.load_stock_price_history(wallet_US.get_tickers(), history)
fileIO.load_stock_price_history('IPCA', history)
fileIO.load_stock_price_history('BVSP', history)
fileIO.load_stock_price_history('USD2BRL', history)

# Create the Processor to aggregate the information contained in Wallet and
# in History
processor = Processor([wallet_BR, wallet_US], history)

# Generate the up-to-date results
df = processor.table_results()
processor.plot_results(aggregate=True)


