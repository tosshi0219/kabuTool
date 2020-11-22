# -*- coding: utf-8 -*-
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib
import os
import datetime

import mpl_finance
from matplotlib import ticker
import matplotlib.dates as mdates

import warnings
warnings.filterwarnings('ignore')

from database.models import KabuDatabase
DB = KabuDatabase()

class PlotChart():
    def sma_chart(self, ax, df):
        ax.plot(df['sma5'],label='sma5',c='green')
        ax.plot(df['sma25'],label='sma25',c='purple')
        ax.plot(df['sma50'],label='sma50',c='red')
        ax.legend()
        return ax

    def bb_chart(self, ax, df):
        ax.plot(df['sma25'],label='sma25',c='purple')
        ax.plot(df['bb_upper1'],label='upper1',c='green', alpha = 0.3)
        ax.plot(df['bb_lower1'],label='lower1',c='green', alpha = 0.3)
        ax.plot(df['bb_upper2'],label='upper2',c='orange', alpha = 0.3)
        ax.plot(df['bb_lower2'],label='lower2',c='orange', alpha = 0.3)
        ax.plot(df['bb_upper3'],label='upper3',c='red', alpha = 0.3)
        ax.plot(df['bb_lower3'],label='lower3',c='red', alpha = 0.3)
        ax.legend()
        return ax

    def ichimoku_chart(self, ax, df):
        ax.plot(df['tenkan'],label='tenkan',c = 'red')
        ax.plot(df['kijun'],label='kijun',c = 'skyblue')
        ax.plot(df['chiko'],label='chiko',c = 'purple' )
        ax.plot(df['senko1'],label='senko1',c = 'green')
        ax.plot(df['senko2'],label='senko2',c = 'lightgreen')
        ax.legend()
        return ax
    
    def macd_chart(self, ax, df):
        ax.plot(df['macd'],label='macd', c = 'blue')
        ax.plot(df['macdsignal'],label='macdsignal', c = 'red')
        ax.bar(df['macdhist'].index,df['macdhist'] ,label='macdhist', color = 'gray')
        ax.set_ylabel('MACD')
        ax.legend(loc='upper left')
        ax.grid()
        return ax

    def rsi_chart(self, ax, df):
        ax.plot(df['rsi9'],label='rsi9', c = 'blue')
        ax.plot(df['rsi14'],label='rsi14', c = 'red')
        ax.set_ylabel('RSI')
        ax.legend(loc='upper left')
        ax.grid()
        ax.set_ylim(0,100)
        ax.axhspan(30,70 ,color = 'purple', alpha = 0.3)
        return ax
    
    def rci_chart(self, ax, df):
        ax.plot(df['rci'],label='rci9', c = 'blue')
        ax.set_ylabel('RCI')
        ax.legend(loc='upper left')
        ax.grid()
        ax.set_ylim(-100,100)
        return ax

    def volume_chart(self, ax, df):
        ax.bar(df.index, df['volume'])
        ax.set_ylabel('volume')
        ax.grid()
        return ax
    
    def simple_candlechart(self, fig, df):
        df.index = mdates.date2num(df.index)
        data = df.reset_index().values
        ax = fig.add_axes((0, 0.6, 1, 0.4))
        mpl_finance.candlestick_ohlc(ax, data, width=0.9, alpha=1, colorup='r', colordown='b')
        return fig, ax
    
    def candlechart_onchart_indicator(self, fig, df, ind = ['sma']):
        fig, ax = self.simple_candlechart(fig, df)
        if 'sma' in ind:
            ax = self.sma_chart(ax,df)
        if 'bb' in ind:
            ax = self.bb_chart(ax,df)
        if 'ichimoku' in ind:
            ax = self.ichimoku_chart(ax,df)
        ax.legend(loc='upper left')
        return fig, ax

    def candlechart_with_dekidaka(self, fig, df, minimum, maximum, dekidaka, width=0.8):
        fig, ax = self.simple_candlechart(fig, df)
        y_range = maximum-minimum
        bar_height = y_range/len(dekidaka)*0.8
        ax1 = ax.twiny()
        ax1.barh(dekidaka.index, dekidaka['volume'],color = 'gray', height = bar_height, alpha=0.4)
        return fig, ax, ax1

    def candlechart_onchart_indicator_with_dekidaka(self, fig, df, minimum, maximum, dekidaka, ind = ['sma'], width=0.8):
        fig, ax = self.candlechart_onchart_indicator(fig, df, ind)
        y_range = maximum-minimum
        bar_height = y_range/len(dekidaka)*0.8
        ax1 = ax.twiny()
        ax1.barh(dekidaka.index, dekidaka['volume'],color = 'gray', height = bar_height, alpha=0.4)
        return fig, ax, ax1
    
    def oscillator(self, fig, ax, df):
        ax0 = fig.add_axes((0, 0.45, 1, 0.15), sharex=ax)
        ax1 = fig.add_axes((0, 0.3, 1, 0.15), sharex=ax)
        ax2 = fig.add_axes((0, 0.15, 1, 0.15), sharex=ax)
        ax3 = fig.add_axes((0, 0, 1, 0.15), sharex=ax)
        ax0 = self.volume_chart(ax0, df)
        ax1 = self.macd_chart(ax1, df)
        ax2 = self.rsi_chart(ax2, df)
        ax3 = self.rci_chart(ax3, df)
        ax.tick_params(labelbottom="off")
        ax0.tick_params(labelbottom="off")
        ax1.tick_params(labelbottom="off")
        ax2.tick_params(labelbottom="off")
        return fig, ax, ax0, ax1, ax2, ax3

    def optional_shodo(self, fig, ax, df, code):
        from get_shodo import CreateShodo
        CS = CreateShodo()
        shodo_info = CS.df_dropdup        
        shodo_date = pd.to_datetime(shodo_info.loc[shodo_info['code']==str(code),'date'].values[0])
        shodo_date_ = mdates.date2num(shodo_date)
        ax.axvline(shodo_date_, color = 'orange', linestyle = '--')
        
        shodo_price = df.loc[df.index == shodo_date,'close'].values[0]
        current_price = df.iloc[-1,df.columns.get_loc('close')]

        if shodo_price >= current_price:
            ax.axhspan(current_price, shodo_price, color='skyblue',alpha=0.5)
        elif shodo_price < current_price:
            ax.axhspan(shodo_price, current_price ,color='pink',alpha=0.5)
            
        return fig, ax, shodo_date, shodo_price, current_price
    
    def optional_kessan(self, fig, ax, df, code, kijun_flg = False, kijun_date = '2019-05-24',
                        current_date = datetime.datetime.today().date()):
        #決算情報表示
        kessan_info = DB.get_dataframe('kessancalendar')
        kessan_info = kessan_info.sort_values('date')
        try:
            kessan_date = kessan_info.loc[kessan_info['code'] == str(code),'date'].values[-1]
            kessan_date = datetime.datetime.strptime(kessan_date, '%Y/%m/%d')
            kessan_term = kessan_info[kessan_info['code'] == str(code)]['quarter'].values[-1]
            kessan_date_ = mdates.date2num(kessan_date)
            ax.axvline(kessan_date_,color = 'skyblue',linestyle = '--',linewidth = 2,label = kessan_term)
        except:
            pass

        try:
            kijun_date = datetime.datetime.strptime(kijun_date, '%Y-%m-%d')
            kijun_date_ = mdates.date2num(kijun_date)
            kijun_price = df.loc[df.index == kijun_date,'close'].values[0]
        except:
            kijun_price = None
        
        current_price = df.loc[current_date,'close']

        if kijun_price is not None:
            if kijun_flg:
                ax.axvline(kijun_date_,color = 'orange',linestyle = '--',linewidth = 2)
                if kijun_price >= current_price:
                    ax.axhspan(current_price, kijun_price, color='skyblue',alpha=0.5)
                elif kijun_price < current_price:
                    ax.axhspan(kijun_price, current_price ,color='pink',alpha=0.5)

        ax.legend()
        return fig, ax, kijun_price, current_price
    
    def optional_kessan_before_after(self,fig, ax, df, code, name):
        kessan_info = DB.get_dataframe('kessancalendar')
        kessan_info = kessan_info.sort_values('date')
        
        flg = True
        d = 0
        while flg:
            try:
                kessan_date = kessan_info.loc[kessan_info['code'] == str(code),'date'].values[-1]
                kessan_date = datetime.datetime.strptime(kessan_date, '%Y/%m/%d')
                kessan_term = kessan_info[kessan_info['code'] == str(code)]['quarter'].values[-1]
                kessan_date = kessan_date - datetime.timedelta(days = d)
                kessan_before_price = df.loc[kessan_date,'close']
                flg = False
            except:
                d -= 1
                flg = True
        
        flg = True
        d = 1
        while flg:
            try:
                kessan_next_date = kessan_date + datetime.timedelta(days = d)
                kessan_after_price = df.loc[kessan_next_date,'close']
                flg = False
            except:
                d += 1
                flg = True
                
        try:
            kessan_date_ = mdates.date2num(kessan_date)
            kessan_next_date_ = mdates.date2num(kessan_next_date)
            ax.axvline(kessan_date_,color = 'skyblue',linestyle = '--',linewidth = 2,label = kessan_term)
        except:
            pass        

        if kessan_before_price >= kessan_after_price:
            ax.axhspan(kessan_before_price, kessan_after_price, color='skyblue',alpha=0.5)
        elif kessan_before_price < kessan_after_price:
            ax.axhspan(kessan_before_price, kessan_after_price ,color='pink',alpha=0.5)
        ax.legend()
        return fig, ax, kessan_before_price, kessan_after_price, kessan_date, kessan_term 

