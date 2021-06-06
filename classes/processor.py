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
    
    def __init__(self, wallets, history):
        self.wallet = wallets
        self.history = history
        self.date1 = min([wallet.get_first_date()[:-2]+'01' for wallet in self.wallet])
        
    def calculate_wallet_value(self, date1=None, date2=None):
        if date1 is None:
            date1 = self.date1
        if date2 is None:
            date2 = dt.datetime.now().strftime('%Y-%m-%d')
        dates = pd.bdate_range(date1, date2).strftime('%Y-%m-%d').to_list()
        wallet_timeseriess = []
        for wallet in self.wallet:
            wallet_timeseries = pd.DataFrame(columns=['Value', 'Cost'])
            for date in dates:
                if wallet.country == 'united states':
                    currency = self.history.get_value_stock(date, 'USD2BRL')
                else:
                    currency = 1
                wallet_timeseries.loc[date] = [
                    self.history.get_value_wallet(date, wallet)*currency,
                    wallet.get_cost(date)*currency]
            
            wallet_timeseries['Profit'] = ((wallet_timeseries['Value']
                                            - wallet_timeseries['Cost'])
                                           /wallet_timeseries['Cost']
                                           .clip(0.001, None)*100)
            wallet_timeseriess.append(wallet_timeseries)
        return wallet_timeseriess
    
    def table_results(self, date=None):
        if date is None:
            date = dt.datetime.now().strftime('%Y-%m-%d')

        dfs = []
        for wallet in self.wallet:
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
            wallet_value = self.history.get_value_wallet(date, wallet)
            for stock in wallet.list_stocks:
                amount, cost = stock.get_amount_cost(date)
                dividends = stock.get_dividends(date)
                price = self.history.get_value_stock(date, stock.ticker)
                if wallet.country == 'united states':
                    price = price * self.history.get_value_stock(date, 'USD2BRL')
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
            cost = df['Total Cost'].sum()
            value = df['Current Value'].sum()
            dividends = df['Dividends'].sum()
            value2 = value + dividends
            date_start = df['Date Start'].min()
            n_days = (dt.datetime.strptime(date, '%Y-%m-%d') -
                      dt.datetime.strptime(date_start, '%Y-%m-%d')).days
            df.loc['Wallet Total'] = [np.nan, 
                                   np.nan,
                                   np.nan,
                                   cost,
                                   value,
                                   dividends,
                                   date_start,
                                   100,
                                   (value2-cost)/cost*100,
                                   ((value2/cost)**(30/n_days) - 1)*100]
            for col in ['Current Price',
                        'Avg. Price',
                        'Total Cost',
                        'Current Value',
                        'Dividends']:
                df[col] = df[col].round(2)
            for col in ['Wallet %', 'Total Earnings (%)', 'Monthly Earnings (%)']:
                df[col] = df[col].round(1)
            dfs.append(df)
        return dfs
    
    def plot_results(self, date1=None, date2=None, aggregate=True):
        if date1 is None:
            date1 = self.date1
        if date2 is None:
            date2 = dt.datetime.now().strftime('%Y-%m-%d')
        # Get the values over time
        wallet_timeseriess = self.calculate_wallet_value(date1, date2)
        if aggregate:
            wallet_timeseriess = [sum(wallet_timeseriess)]
        for wallet_timeseries in wallet_timeseriess:
            # Get the 'weekly' values
            wallet_timeseries2 = wallet_timeseries.copy()
            wallet_timeseries2.index = pd.to_datetime(wallet_timeseries.index)
            wallet_timeseries2['weekday'] = wallet_timeseries2.index.dayofweek
            wallet_timeseries2 = \
                wallet_timeseries2.loc[wallet_timeseries2['weekday']==4,:]
            wallet_timeseries2.index = wallet_timeseries2.index.strftime('%Y-%m-%d')
            # Get the IPCA values
            ipca = self.history.data['IPCA']
            ipca = ipca.loc[(ipca.index>=date1) & (ipca.index<=date2), :]
            ipca.at[ipca.index[0],'Value'] = 0
            # Get the BVSP values
            try:
                bvsp = self.history.data['BVSP']
                bvsp = bvsp.loc[(bvsp.index>=date1) & (bvsp.index<=date2), :]
                bvsp = bvsp/bvsp.iloc[0,0]-1
            except:
                bvsp = None    
            
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
            # tick_dates2 = [self.get_nearest_date(date, wallet_timeseries2) 
            #                for date in tick_labels]
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
            if bvsp is not None:
                df2 = pd.concat([wallet_timeseries[['Profit']], 
                                 ((1+ipca/100+(1.04**(1/12)-1)).cumprod()-1)*100,
                                 ((1+ipca/100+(1.06**(1/12)-1)).cumprod()-1)*100,
                                 bvsp[['Price']]], axis=1).sort_index()
            else:
                df2 = pd.concat([wallet_timeseries[['Profit']], 
                                 ((1+ipca/100+(1.04**(1/12)-1)).cumprod()-1)*100,
                                 ((1+ipca/100+(1.06**(1/12)-1)).cumprod()-1)*100
                                ], axis=1).sort_index()
            plt.plot(df2.iloc[:,0], 'C0', label=None, zorder=10)
            plt.plot(df2.iloc[:,0].dropna(), 'C0', label='Wallet', zorder=10)
            plt.plot(df2.iloc[:,1].dropna(), 'C1', label='IPCA+4%', zorder=5)
            plt.plot(df2.iloc[:,2].dropna(), 'C3', label='IPCA+6%', zorder=5)
            if bvsp is not None:
                plt.plot(df2.iloc[:,3].dropna()*100, 'C2', label='BVSP', zorder=0)
            plt.xticks(tick_dates, tick_labels, rotation=45, ha='right', 
                       fontsize=9)
            plt.grid()
            plt.ylabel('Total Earnings (%)')
            plt.legend()
            plt.tight_layout()
        
            # # Plot the variation over weeks
            # plt.figure(figsize=figsize)
            # ax1 = plt.gca()
            # ax1.bar(wallet_timeseries2.index, wallet_timeseries2['Profit'].diff(),
            #         width=1)
            # ax1.set_ylabel('Weekly Variation of Wallet (%)')
            # plt.grid()
            # ax2 = plt.gca().twinx()
            # ax2.plot(wallet_timeseries2.index, 
            #           ((wallet_timeseries2['Profit'].diff()/100 + 1
            #             ).cumprod() - 1)*100, 'gray')
            # ax2.set_ylabel('Accumulated Earnings (%)')
            # ax1.set_zorder(ax2.get_zorder()+5)
            # ax1.patch.set_visible(False)
            # ax1.set_xticks(tick_dates2)
            # ax1.set_xticklabels(tick_labels, rotation=45, ha='right', 
            #             fontsize=9)
            # plt.tight_layout()
        
        
    def get_nearest_date(self, date, data):
        if date in data.index:
            return date
        else:
            return data.index[data.index>=date][0]
