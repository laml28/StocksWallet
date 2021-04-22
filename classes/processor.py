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
        wallet_timeseries = pd.DataFrame(columns=['Value', 'Cost'])
        for date in dates:
            # value.loc[date] = self.history.get_value_wallet(date, self.wallet)
            # cost.loc[date] = self.wallet.get_cost(date)
            wallet_timeseries.loc[date] = [
                self.history.get_value_wallet(date, self.wallet),
                self.wallet.get_cost(date)]
        # profit = (value['Value' - cost)/cost.clip(0.001, None)*100
        wallet_timeseries['Profit'] = ((wallet_timeseries['Value']
                                        - wallet_timeseries['Cost'])
                                       /wallet_timeseries['Cost']
                                       .clip(0.001, None)*100)
        return wallet_timeseries
    
    def table_results(self, date):
        df = pd.DataFrame(columns=['Current Price',
                                   'Amount',
                                   'Avg. Price',
                                   'Total Cost',
                                   'Current Value',
                                   'Dividends',
                                   'Date Start',
                                   'Wallet %',
                                   'Total Earnings (%)',
                                   'Monthly Earnings (%)'])
        df.index.name = 'Stock'
        wallet_value = self.history.get_value_wallet(date, self.wallet)
        for stock in self.wallet.list_stocks:
            amount, cost = stock.get_amount_cost(date)
            dividends = stock.get_dividends(date)
            price = self.history.get_value_stock(date, stock.ticker)
            value = price*amount
            value2 = value + dividends
            date_start = stock.get_first_date()
            n_days = (dt.datetime.strptime(date, '%Y-%m-%d') -
                      dt.datetime.strptime(date_start, '%Y-%m-%d')).days
            df.loc[stock.ticker] = [price,
                                    amount,
                                    cost/amount,
                                    cost,
                                    value,
                                    dividends,
                                    date_start,
                                    value2/wallet_value*100,
                                    (value2-cost)/cost*100,
                                    ((value2/cost)**(30/n_days) - 1)*100]
        df = df.sort_index()
        for col in ['Current Price',
                    'Avg. Price',
                    'Total Cost',
                    'Current Value',
                    'Dividends']:
            df[col] = df[col].round(2)
        for col in ['Wallet %', 'Total Earnings (%)', 'Monthly Earnings (%)']:
            df[col] = df[col].round(1)
        return df
    
    def plot_results(self, date1=None, date2=None):
        if date1 is None:
            date1 = self.date1
        if date2 is None:
            date2 = dt.datetime.now().strftime('%Y-%m-%d')
        # Get the values over time
        wallet_timeseries = self.calculate_wallet_value(date1, date2)
        # Get the 'weekly' values
        wallet_timeseries2 = wallet_timeseries.copy()
        wallet_timeseries2.index = pd.to_datetime(wallet_timeseries.index)
        wallet_timeseries2['weekday'] = wallet_timeseries2.index.dayofweek
        wallet_timeseries2 = \
            wallet_timeseries2.loc[wallet_timeseries2['weekday']==4,:]
        wallet_timeseries2.index = wallet_timeseries2.index.strftime('%Y-%m-%d')
        
        # Adjust the plot x ticks
        years = list(range(int(date1[:4]), int(date2[:4])+1))
        months = ['01', '04', '07', '10']
        tick_labels = ['{}-{}'.format(year, mon) for year in years 
                       for mon in months]
        tick_labels = [date for date in tick_labels if date>=date1 
                       and date <= date2]
        tick_labels.sort()
        tick_dates = [self.get_nearest_date(date, wallet_timeseries) 
                      for date in tick_labels]
        tick_dates2 = [self.get_nearest_date(date, wallet_timeseries2) 
                       for date in tick_labels]
        figsize = (5,3)
        # Plot the wallet value and invested money
        plt.figure(figsize=figsize)
        plt.plot(wallet_timeseries['Cost']/1000, 'C1', label='Invested')
        plt.plot(wallet_timeseries['Value']/1000, 'C0', label='Value')
        plt.xticks(tick_dates, tick_labels, rotation=45, ha='right', 
                   fontsize=9)
        plt.grid()
        plt.ylabel('Wallet Value (k R$)')
        plt.legend()
        plt.tight_layout()
        # Plot the total earnings
        plt.figure(figsize=figsize)
        plt.plot(wallet_timeseries['Profit'])
        plt.xticks(tick_dates, tick_labels, rotation=45, ha='right', 
                   fontsize=9)
        plt.grid()
        plt.ylabel('Total Earnings (%)')
        plt.tight_layout()
        # Plot the variation over weeks
        plt.figure(figsize=figsize)
        ax1 = plt.gca()
        ax1.bar(wallet_timeseries2.index, wallet_timeseries2['Profit'].diff(),
                width=1)
        ax1.set_ylabel('Weekly Variation of Wallet (%)')
        plt.grid()
        ax2 = plt.gca().twinx()
        ax2.plot(wallet_timeseries2.index, 
                  ((wallet_timeseries2['Profit'].diff()/100 + 1
                    ).cumprod() - 1)*100, 'gray')
        ax2.set_ylabel('Accumulated Earnings (%)')
        ax1.set_zorder(ax2.get_zorder()+5)
        ax1.patch.set_visible(False)
        ax1.set_xticks(tick_dates2)
        ax1.set_xticklabels(tick_labels, rotation=45, ha='right', 
                    fontsize=9)
        plt.tight_layout()
        #


        
        
    def get_nearest_date(self, date, data):
        if date in data.index:
            return date
        else:
            return data.index[data.index>=date][0]
