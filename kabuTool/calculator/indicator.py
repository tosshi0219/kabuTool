# -*- coding: utf-8 -*-
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib
import os

import mpl_finance
from matplotlib import ticker
import matplotlib.dates as mdates

import sys
args = sys.argv

import warnings
warnings.filterwarnings('ignore')

class Indicator():
    def RCI(self,close, timeperiod = 9):
        '''
        RCI＝(1-(6×d)÷(nの3乗-n))×100
        d：「日付の順位」と「価格の順位」の差を2乗し、合計した数値
        n：期間
        日付の順位：当日(最新の日付)＝1、として遡りながら、2,3,4・・・と順位をつけます
        価格の順位：期間中の最高値＝1、として、高い順に2,3,4・・・と順位をつけます
        '''
        rci = []
        for j in range(len(close)):
            if j < timeperiod:
                rci.append(np.nan)
            else:
                data = pd.DataFrame()
                data['close'] = list(close[j-timeperiod:j])
                data = data.reset_index()
                data = data.rename(columns = {'index':'original_index'})
                data = data.sort_values('close',ascending=False).reset_index(drop = True)
                data = data.reset_index()
                data['index'] = [i+1 for i in data['index']]
                data = data.rename(columns = {'index':'price_rank'})
                data = data.set_index('original_index')
                data = data.sort_index()
                data['date_rank'] = np.arange(timeperiod,0,-1)
                data['delta'] = [(data.loc[ii,'price_rank']-data.loc[ii,'date_rank'])**2 for ii in range(len(data))]
                d = data['delta'].sum()
                value = (1-(6*d)/(timeperiod**3-timeperiod))*100
                rci.append(value)
        return rci

    def ichimoku(self,close):
        max9 = close.rolling(9).max()
        min9 = close.rolling(9).min()
        max26 = close.rolling(26).max()
        min26 = close.rolling(26).min()
        max52 = close.rolling(52).max()
        min52 = close.rolling(52).min()

        kijun = (max26 + min26) / 2
        tenkan = (max9 + min9) / 2

        chiko = close.copy()
        chiko_index = np.arange(-26,len(close)-26)
        chiko.index = chiko_index

        senko1 = (tenkan + kijun) / 2
        senko2 = (max52 + min52) / 2
        senko_index = np.arange(26,len(close)+26)
        senko1.index = senko_index
        senko2.index = senko_index

        return tenkan,kijun,chiko,senko1,senko2

    #価格帯別出来高の計算
    def kakakutai_dekidaka(self,df):
        OPEN = df['open']
        HIGH = df['high']
        LOW = df['low']
        CLOSE = df['close']
        VOLUME = df['volume']

        #1日の平均価格を計算
        ave = talib.AVGPRICE(OPEN, HIGH, LOW, CLOSE)

        #価格のレンジを確認
        minimum = np.floor(LOW.min())
        maximum = np.ceil(HIGH.max())
#         print('価格のレンジ：{}-{}'.format(minimum,maximum))

        #価格のレンジをビン分割する
        supposed_bin_num = 20
        bin_range = int(np.ceil((maximum - minimum)/supposed_bin_num))
#         print('各価格帯の刻み：{}'.format(bin_range))

        #ビン分割の境界値のリストとリストの長さ
        bins = np.arange(minimum,maximum,bin_range)
#         print('境界値リスト：{}'.format(bins))
#         print('境界値リスト長さ：{}'.format(len(bins)))

        #1日の平均価格をビン分割
        cut = pd.cut(ave, bins)

        #出来高データと統合
        data = pd.DataFrame()
        data['cut'] = cut
        data['axis'] = cut.apply(lambda x: x.mid)
        data['volume'] = VOLUME

        #価格帯別の出来高を合計する
        dekidaka = data.groupby('axis').sum()
        dekidaka.fillna(0)
        return minimum, maximum,dekidaka

    def ohlc_with_indicator(self, df):
        OPEN = df['open']
        HIGH = df['high']
        LOW = df['low']
        CLOSE = df['close']
        VOLUME = df['volume']

        #Simple Moving Average
        sma5 = talib.SMA(CLOSE, timeperiod=5)
        sma25 = talib.SMA(CLOSE, timeperiod=25)
        sma50 = talib.SMA(CLOSE, timeperiod=50)
        sma75 = talib.SMA(CLOSE, timeperiod=75)
        sma100 = talib.SMA(CLOSE, timeperiod=100)

        #Bollinger Bands
        upper1, middle,lower1 = talib.BBANDS(CLOSE, timeperiod=25, nbdevup=1, nbdevdn=1, matype=0)
        upper2, middle, lower2 = talib.BBANDS(CLOSE, timeperiod=25, nbdevup=2, nbdevdn=2, matype=0)
        upper3, middle, lower3 = talib.BBANDS(CLOSE, timeperiod=25, nbdevup=3, nbdevdn=3, matype=0)

        #MACD - Moving Average Convergence/Divergence
        macd, macdsignal, macdhist = talib.MACD(CLOSE, fastperiod=12, slowperiod=26, signalperiod=9)

        #RSI - Relative Strength Index
        rsi9 = talib.RSI(CLOSE, timeperiod=9)
        rsi14 = talib.RSI(CLOSE, timeperiod=14)

        #Ichimoku
        tenkan,kijun,chiko,senko1,senko2 = self.ichimoku(CLOSE)
        tenkan = pd.DataFrame(tenkan).rename(columns = {'close':'tenkan'})
        kijun = pd.DataFrame(kijun).rename(columns = {'close':'kijun'})
        chiko = pd.DataFrame(chiko).rename(columns = {'close':'chiko'})
        senko1 = pd.DataFrame(senko1).rename(columns = {'close':'senko1'})
        senko2 = pd.DataFrame(senko2).rename(columns = {'close':'senko2'})

        #RCI
        rci9 = self.RCI(CLOSE)

        df['sma5'] = sma5
        df['sma25'] = sma25
        df['sma50'] = sma50
        df['sma75'] = sma75
        df['sma100'] = sma100
        df['bb_upper1'] = upper1
        df['bb_upper2'] = upper2
        df['bb_upper3'] = upper3
        df['bb_lower1'] = lower1
        df['bb_lower2'] = lower2
        df['bb_lower3'] = lower3
        df['macd'] = macd
        df['macdsignal'] = macdsignal
        df['macdhist'] = macdhist
        df['rsi9'] = rsi9
        df['rsi14'] = rsi14
        df['rci'] = rci9

        df = df.join(tenkan)
        df = df.join(kijun)
        df = df.join(chiko,how = 'outer')
        df = df.join(senko1,how = 'outer')
        df = df.join(senko2,how = 'outer')

        df = df[df['date'] == df['date']]
        return df

if __name__ == '__main__':
    #設定情報
    LOOKBACK = 120 #対象期間
#     LOOKBACK =int(args[2]) #対象期間

    #辞書データフレームのロード
#     list_name = args[1]
    list_name = 'vol1'
    print(list_name)
    if list_name == 'vol1':
        target_csv = '/10baikabu1_list.csv'
    elif list_name == 'vol2':
        target_csv = '/10baikabu2_list.csv'

    load_directory = 'kabuka'
    dic_df = pd.read_csv(load_directory + target_csv)

#     for i in dic_df.index:
    for i in range(1):
        k, v = dic_df.loc[i,'code'], dic_df.loc[i,'name']
        print(k, v)

        load_path = load_directory + '/{}-{}.csv'.format(k,v)
        df = pd.read_csv(load_path)

        IND = Indicator()
        df = IND.ohlc_with_indicator(df)
        minimum, maximum, dekidaka = IND.kakakutai_dekidaka(df)
        print(df)
