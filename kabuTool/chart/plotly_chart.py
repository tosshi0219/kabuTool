import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly as py
import plotly.figure_factory as ff
import json

def candle_data(_df):
    x = np.arange(len(_df))
    data = go.Candlestick(
                    x = x,
                    open=_df['open'],
                    high=_df['high'],
                    low=_df['low'],
                    close=_df['close'],
                    hovertext= ['date:{}<br>open:{}<br>high:{}<br>low:{}<br>close:{}'
                                       .format(_df.loc[i,'date'],_df.loc[i,'open'],_df.loc[i,'high'],_df.loc[i,'low'],_df.loc[i,'close']) for i in range(len(_df))] ,
                    hoverinfo="text",
                    increasing = dict(
                            line_width = 1,
                            line_color='#E61C1C',
                            fillcolor='#E61C1C',
                     ),
                    decreasing = dict(
                            line_width = 1,
                            line_color='#2DBD3F',
                            fillcolor='#2DBD3F'
                     )
    )
    return data

def get_yrange(_df):
    margin = 1.2
    r = (_df.high.max() - _df.low.min())/2*margin
    m = (_df.high.max() + _df.low.min())/2
    y_l = m - r
    y_u = m + r
    return y_l, y_u


def plot_layout(_df, _code, _name):
    interval = 20
    iter_num = len(_df)//interval
    iter_mod = len(_df)%interval
    if iter_mod != 0:
        iter_num = iter_num + 1

    vals = [_df.index[i*interval] for i in range(iter_num)]
    labels = [_df.loc[i*interval,'date'] for i in range(iter_num)]

  #y軸範囲設定
    y_l, y_u = get_yrange(_df)
    
    return go.Layout(
#                     title = _code + ' ' + _name,
                    height = 300,
#                     width = 900,
                    margin=dict(l=20, r=20, t=45, b=20),
                    xaxis = dict(
                        ticktext = labels,
                        tickvals = vals,
                        tickangle=-45,
                        showgrid = True,
                        zeroline=False,
                        ),
                    yaxis = dict(
                        showgrid = True,
                        zeroline=False,
                        range = (y_l,y_u)
                        ),
                    xaxis_rangeslider_visible=False,
                    showlegend = False
                )



def plot_candle_chart(_data, _layout):
    fig = go.Figure(
            data=_data,
            layout = _layout
            )
    return json.dumps(fig, cls=py.utils.PlotlyJSONEncoder)

    # fig.show()
