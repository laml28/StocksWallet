# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 00:56:45 2021

@author: DECO
"""

import pandas as pd
import datetime as dt
import os

import investpy

from classes.stock import Stock
from classes.order import Order
from classes.dividend import Dividend
from classes.wallet import Wallet
from classes.history import History

class FileIO():
    
    def load_orders(self, path_orders, path_dividends):
        orders = pd.read_csv(path_orders, sep=';', index_col=0, header=0)
        dividends = pd.read_csv(path_dividends, sep=';', index_col=0, header=0)
        list_stocks = []
        for ticker in orders.index.unique():
            list_orders = []
            for row in orders.loc[[ticker]].iterrows():
                list_orders.append(Order(row[1]['Date'], 
                                         row[1]['Amount'],
                                         row[1]['Price'], 
                                         row[1]['Kind']))
            list_dividends = []
            if ticker in dividends.index:
                for row in dividends.loc[[ticker]].iterrows():
                    list_dividends.append(Dividend(row[1]['Date'], 
                                                   row[1]['Value'],
                                                   row[1]['Kind']))
            list_stocks.append(Stock(ticker, list_orders, list_dividends))

        return Wallet(list_stocks)
            
    def update_stocks_price_history(self, tickers, country):
        for ticker in tickers:
            self.update_stock_price_history(ticker, country)

                
    def update_stock_price_history(self, ticker, country):
        # By default get data starting 5 years ago
        today = dt.datetime.now().strftime('%d/%m/%Y')
        begin = (dt.datetime.strptime(today, '%d/%m/%Y') 
                 - dt.timedelta(days=365*5)).strftime('%d/%m/%Y')
        path = 'price_history\\{}.csv'.format(ticker)
        # If some data was already gotten, start from the latest date
        if os.path.isfile(path):
            data0 = pd.read_csv(path, index_col=0, header=0, sep=';')
            data0.index = pd.to_datetime(data0.index)
            begin = (data0.index[-1] + dt.timedelta(days=1)).strftime('%d/%m/%Y')
        else:
            data0 = pd.DataFrame(columns=['Price'],
                                 index=pd.Series([], name='Date'))
        if (dt.datetime.strptime(begin, '%d/%m/%Y') 
            < dt.datetime.strptime(today, '%d/%m/%Y')):
            # try:
            #     data = investpy.get_stock_historical_data(stock=ticker,
            #                                               country=country,
            #                                               from_date=begin,
            #                                               to_date=today)
            # except:
            search_result = investpy.search_quotes(text=ticker, 
                                                   countries=[country],
                                                   n_results=1)
            data = search_result.retrieve_historical_data(
                                    from_date=begin, to_date=today)

            data.index = pd.to_datetime(data.index)
            data = data[['Close']]
            data = data.rename(columns={'Close': 'Price'})
            data = pd.concat([data0, data], axis=0).sort_index()
            data.index = data.index.strftime('%Y-%m-%d')
            data = data.sort_index()
            data.to_csv(path, index=True, header=True, sep=';')
            
    def update_ipca_history(self):
        path = 'price_history\\IPCA.csv'
        # By default get data starting 5 years ago
        today = dt.datetime.now().strftime('%d/%m/%Y')
        if os.path.isfile(path):
            data0 = pd.read_csv(path, index_col=0, header=0, sep=';')
            data0.index = pd.to_datetime(data0.index)
            begin = (data0.index[-1] + dt.timedelta(days=1)).strftime('%d/%m/%Y')
        else:
            data0 = pd.DataFrame(columns=['Value'],
                                 index=pd.Series([], name='Date'))
            begin = (dt.datetime.strptime(today, '%d/%m/%Y') 
                     - dt.timedelta(days=365*5)).strftime('%d/%m/%Y')
        if (dt.datetime.strptime(begin, '%d/%m/%Y') 
            < dt.datetime.strptime(today, '%d/%m/%Y')):
            url = ('http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/'
                   'dados?formato=json&dataInicial={}&dataFinal={}'
                   .format(433, begin, today))
            data = pd.read_json(url)
            data.columns = ['Date', 'Value']
            data = data.set_index('Date')
            data.index = pd.to_datetime(data.index, format='%d/%m/%Y')
            data = pd.concat([data0, data], axis=0).sort_index()
            data.index = data.index.strftime('%Y-%m-%d')
            data = data.sort_index()
            data = data[~data.index.duplicated(keep='first')]
            data.to_csv(path, index=True, header=True, sep=';')

    
    def load_stock_price_history(self, tickers, history):
        if not isinstance(tickers, list):
            tickers = [tickers]
        for ticker in tickers:
            data = pd.read_csv('price_history\\{}.csv'.format(ticker), 
                               index_col=0, header=0, sep=';')
            history.add_data(ticker, data)
            