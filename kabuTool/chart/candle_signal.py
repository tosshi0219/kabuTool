# -*- coding: utf-8 -*-
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_finance as mpf
import matplotlib.dates as mdates 
from matplotlib.dates import date2num
import talib as ta
import datetime

#61種類のローソク足パターンをチェックしたデータフレームの作成
def create_signal_dataframe(df_):
    o = np.array(df_['始値'])
    c = np.array(df_['終値'])
    l = np.array(df_['安値'])
    h = np.array(df_['高値'])
    df = df_.copy()
    df['CDL2CROWS'] = ta.CDL2CROWS(o, h, l, c)
    df['CDL3BLACKCROWS'] = ta.CDL3BLACKCROWS(o, h, l, c)
    df['CDL3INSIDE'] = ta.CDL3INSIDE(o, h, l, c)
    df['CDL3LINESTRIKE'] = ta.CDL3LINESTRIKE(o, h, l, c)
    df['CDL3OUTSIDE'] = ta.CDL3OUTSIDE(o, h, l, c)
    df['CDL3STARSINSOUTH'] = ta.CDL3STARSINSOUTH(o, h, l, c)
    df['CDL3WHITESOLDIERS'] = ta.CDL3WHITESOLDIERS(o, h, l, c)
    df['CDLABANDONEDBABY'] = ta.CDLABANDONEDBABY(o, h, l, c)
    df['CDLADVANCEBLOCK'] = ta.CDLADVANCEBLOCK(o, h, l, c)
    df['CDLBELTHOLD'] = ta.CDLBELTHOLD(o, h, l, c)
    df['CDLBREAKAWAY'] = ta.CDLBREAKAWAY(o, h, l, c)
    df['CDLCLOSINGMARUBOZU'] = ta.CDLCLOSINGMARUBOZU(o, h, l, c)
    df['CDLCONCEALBABYSWALL'] = ta.CDLCONCEALBABYSWALL(o, h, l, c)
    df['CDLCOUNTERATTACK'] = ta.CDLCOUNTERATTACK(o, h, l, c)
    df['CDLDARKCLOUDCOVER'] = ta.CDLDARKCLOUDCOVER(o, h, l, c)
    df['CDLDOJI'] = ta.CDLDOJI(o, h, l, c)
    df['CDLDOJISTAR'] = ta.CDLDOJISTAR(o, h, l, c)
    df['CDLDRAGONFLYDOJI'] = ta.CDLDRAGONFLYDOJI(o, h, l, c)
    df['CDLENGULFING'] = ta.CDLENGULFING(o, h, l, c)
    df['CDLEVENINGDOJISTAR'] = ta.CDLEVENINGDOJISTAR(o, h, l, c)
    df['CDLEVENINGSTAR'] = ta.CDLEVENINGSTAR(o, h, l, c)
    df['CDLGAPSIDESIDEWHITE'] = ta.CDLGAPSIDESIDEWHITE(o, h, l, c)
    df['CDLGRAVESTONEDOJI'] = ta.CDLGRAVESTONEDOJI(o, h, l, c)
    df['CDLHAMMER'] = ta.CDLHAMMER(o, h, l, c)
    df['CDLHANGINGMAN'] = ta.CDLHANGINGMAN(o, h, l, c)
    df['CDLHARAMI'] = ta.CDLHARAMI(o, h, l, c)
    df['CDLHARAMICROSS'] = ta.CDLHARAMICROSS(o, h, l, c)
    df['CDLHIGHWAVE'] = ta.CDLHIGHWAVE(o, h, l, c)
    df['CDLHIKKAKE'] = ta.CDLHIKKAKE(o, h, l, c)
    df['CDLHIKKAKEMOD'] = ta.CDLHIKKAKEMOD(o, h, l, c)
    df['CDLHOMINGPIGEON'] = ta.CDLHOMINGPIGEON(o, h, l, c)
    df['CDLIDENTICAL3CROWS'] = ta.CDLIDENTICAL3CROWS(o, h, l, c)
    df['CDLINNECK'] = ta.CDLINNECK(o, h, l, c)
    df['CDLINVERTEDHAMMER'] = ta.CDLINVERTEDHAMMER(o, h, l, c)
    df['CDLKICKING'] = ta.CDLKICKING(o, h, l, c)
    df['CDLKICKINGBYLENGTH'] = ta.CDLKICKINGBYLENGTH(o, h, l, c)
    df['CDLLADDERBOTTOM'] = ta.CDLLADDERBOTTOM(o, h, l, c)
    df['CDLLONGLEGGEDDOJI'] = ta.CDLLONGLEGGEDDOJI(o, h, l, c)
    df['CDLLONGLINE'] = ta.CDLLONGLINE(o, h, l, c)
    df['CDLMARUBOZU'] = ta.CDLMARUBOZU(o, h, l, c)
    df['CDLMATCHINGLOW'] = ta.CDLMATCHINGLOW(o, h, l, c)
    df['CDLMATHOLD'] = ta.CDLMATHOLD(o, h, l, c)
    df['CDLMORNINGDOJISTAR'] = ta.CDLMORNINGDOJISTAR(o, h, l, c)
    df['CDLMORNINGSTAR'] = ta.CDLMORNINGSTAR(o, h, l, c)
    df['CDLONNECK'] = ta.CDLONNECK(o, h, l, c)
    df['CDLPIERCING'] = ta.CDLPIERCING(o, h, l, c)
    df['CDLRICKSHAWMAN'] = ta.CDLRICKSHAWMAN(o, h, l, c)
    df['CDLRISEFALL3METHODS'] = ta.CDLRISEFALL3METHODS(o, h, l, c)
    df['CDLSEPARATINGLINES'] = ta.CDLSEPARATINGLINES(o, h, l, c)
    df['CDLSHOOTINGSTAR'] = ta.CDLSHOOTINGSTAR(o, h, l, c)
    df['CDLSHORTLINE'] = ta.CDLSHORTLINE(o, h, l, c)
    df['CDLSPINNINGTOP'] = ta.CDLSPINNINGTOP(o, h, l, c)
    df['CDLSTALLEDPATTERN'] = ta.CDLSTALLEDPATTERN(o, h, l, c)
    df['CDLSTICKSANDWICH'] = ta.CDLSTICKSANDWICH(o, h, l, c)
    df['CDLTAKURI'] = ta.CDLTAKURI(o, h, l, c)
    df['CDLTASUKIGAP'] = ta.CDLTASUKIGAP(o, h, l, c)
    df['CDLTHRUSTING'] = ta.CDLTHRUSTING(o, h, l, c)
    df['CDLTRISTAR'] = ta.CDLTRISTAR(o, h, l, c)
    df['CDLUNIQUE3RIVER'] = ta.CDLUNIQUE3RIVER(o, h, l, c)
    df['CDLUPSIDEGAP2CROWS'] = ta.CDLUPSIDEGAP2CROWS(o, h, l, c)
    df['CDLXSIDEGAP3METHODS'] = ta.CDLXSIDEGAP3METHODS(o, h, l, c)
    return df
    
#candle masterをloadし、綺麗にして引き渡す関数
def load_candle_master():
    candle_master = pd.read_excel('candle_chart_master.xlsx',header = 1)
    candle_master = candle_master.reset_index(drop=True)

    #売りシグナルのTA-Lib関数がnanになっているので埋める
    for i,v in enumerate(candle_master['TA-Lib関数']):
        if v != v:
            candle_master.iloc[i,7] = candle_master.iloc[i-1,7]

    #不要なnanの行は削除
    candle_master = candle_master[candle_master['ローソク足タイプ（英語）']==candle_master['ローソク足タイプ（英語）']]

    #不要なタイトル行は削除
    candle_master = candle_master[candle_master['TA-Lib関数']!='TA-Lib関数']

    #TA-Lib関数の文字列を編集
    candle_master['TA-Lib関数'] = [i.split('= ')[1] for i in candle_master['TA-Lib関数']]
    candle_master['TA-Lib関数'] = [i.split('(')[0] for i in candle_master['TA-Lib関数']]

    #nanの箇所を'-'で埋める
    candle_master = candle_master.fillna('-').set_index('TA-Lib関数')

    #不要な売買シグナルは削除
    unnecessary_signal = list(candle_master[candle_master['サイン']=='-'].index)
    candle_master = candle_master.drop(unnecessary_signal)

    #必要な項目だけにする
    candle_master = candle_master.drop(['No','ローソク足形状','説明','TA-Lib関数名'],axis=1)

    #買いシグナルと売りシグナルでmasterを分ける
    bullish_candle_master = candle_master[candle_master['サイン']=='買い']
    bearish_candle_master = candle_master[candle_master['サイン']=='売り']
    return candle_master,bullish_candle_master,bearish_candle_master

def delete_unnecessary_columns(df,candle_master):
    candle_col = ['日付','始値','高値','安値','終値','出来高','終値調整']
    candle_col.extend(list(set(list(candle_master.index))))
    df = df.loc[:,candle_col]
    return df

def alart_signal(k,v,df):
    bullish_signal_col = [col for col in bullish_candle_master.index if df.loc[df.index[-1],col] > 0]
    bearish_signal_col = [col for col in bearish_candle_master.index if df.loc[df.index[-1],col] < 0]

    if len(bullish_signal_col) != 0:
        for s in bullish_signal_col:
            print(k,v,bullish_candle_master.loc[s,'ローソク足タイプ(日本語）'],bullish_candle_master.loc[s,'サイン']) 

    elif len(bearish_signal_col) != 0:
        for s in bearish_signal_col:
            print(k,v,bearish_candle_master.loc[s,'ローソク足タイプ(日本語）'],bearish_candle_master.loc[s,'サイン']) 
    else:
        pass
#         print(k,v,'シグナルなし')

# load_directory = 'kabuka'
# with open(load_directory + '/dic.pkl', mode='rb') as f:
#     dic = pickle.load(f)
    
# candle_master,bullish_candle_master,bearish_candle_master = load_candle_master()
# dfs = []
# for k,v in dic.items():
#     load_path = load_directory + '/{}-{}.pkl'.format(k,v)
    
#     with open(load_path, mode='rb') as f:
#         d = pickle.load(f)
        
#     df = create_signal_dataframe(d)
#     df = delete_unnecessary_columns(df,candle_master)

#     alart_signal(k,v,df)

# print('https://non-dimension.com/2019/06/16/candle-signal-check/')