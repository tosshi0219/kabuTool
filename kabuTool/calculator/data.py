from datetime import datetime, timedelta
import pandas as pd

DATE = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4
VOLUME = 5

class Data():
    def __init__(self, ohlcv_data, _year=datetime.now().year):
        self.data = ohlcv_data
        self.first_date = self.get_first_date(_year)
        self.last_date = self.get_last_date(_year)
        self.first_working_date, self.first_working_close = self.get_first_working_data()
        self.annual_data = self.filter_data()
        self.working_date = list(self.data.date)
        self.yh, self.yh_idx, self.yh_date = self.calc_yh('high')
        self.yl, self.yl_idx, self.yl_date = self.calc_yl('low')
        self.yh_close, self.yh_close_idx, self.yh_close_date = self.calc_yh('close')
        self.yl_close, self.yl_close_idx, self.yl_close_date = self.calc_yl('close')
#         self.max_drawdown, self.max_drawdown_ratio, self.max_drawdown_st_date, self.max_drawdown_end_date = self.calc_max_drawdown()
#         self.max_increase, self.max_increase_ratio, self.max_increase_st_date, self.max_increase_end_date = self.calc_max_increase()
        
    def get_first_date(self, _year):
        return datetime(_year, 1, 1)

    def get_last_date(self, _year):
        return datetime(_year, 12, 31)
    
    def get_daily_kabuka(self, _date):
        return self.data[self.data.date == _date].reset_index(drop=True)
    
    def get_first_working_data(self):
        first_working_date = self.first_date
        for i in range(365):
            v = self.get_daily_kabuka(first_working_date)
            if len(v) != 0:
                first_working_date =  list(v.date)[0]
                first_working_close = list(v.close)[0]
                return first_working_date, first_working_close
            else:
                first_working_date += timedelta(days=1)        
                        
    def filter_data(self):
        return self.data[(self.data.date >= self.first_working_date) &
                            (self.data.date <= self.last_date)].reset_index(drop=True)
            
    def calc_yh(self, _col):
        yh = self.annual_data[_col].max()
        yh_idx = self.annual_data[_col].idxmax()
        yh_date = self.annual_data.iloc[yh_idx, DATE]  
        return yh, yh_idx, yh_date
    
    def calc_yl(self, _col):
        yl = self.annual_data[_col].min()
        yl_idx = self.annual_data[_col].idxmin()
        yl_date = self.annual_data.iloc[yl_idx, DATE]  
        return yl, yl_idx, yl_date

    def calc_max_drawdown(self):
        df = self.annual_data
        dif = df.close.diff()

        minus_idx = dif[dif < 0].index
        plus_idx = dif[dif > 0].index

        val = []
        for st_idx in minus_idx:
            possible_end_idx = plus_idx[plus_idx > st_idx]
            for end_idx in possible_end_idx:
                val.append([st_idx -1, end_idx -1, dif[st_idx:end_idx].sum()])

        df_val = pd.DataFrame(val, columns = ('st_idx', 'end_idx', 'drawdown'))
        max_drawdown_idx = df_val.drawdown.idxmin()
        st_idx, end_idx, max_drawdown = df_val.iloc[max_drawdown_idx,0], df_val.iloc[max_drawdown_idx,1], df_val.iloc[max_drawdown_idx,2]
        max_drawdown_ratio = max_drawdown/df.iloc[st_idx,CLOSE]
        st_date, end_date = df.iloc[st_idx,:].date, df.iloc[end_idx,:].date
        return {
            'start_date': st_date,
            'end_date': end_date,
            'max_drawdown': max_drawdown,
            'max_drawdown_ratio': max_drawdown_ratio,
        }
    
    def calc_max_increase(self):
        df = self.annual_data
        dif = df.close.diff()

        minus_idx = dif[dif < 0].index
        plus_idx = dif[dif > 0].index
        st_idx = plus_idx[0]
        end_idx = minus_idx[minus_idx > st_idx][0]

        val = []
        for st_idx in plus_idx:
            possible_end_idx = minus_idx[minus_idx > st_idx]
            for end_idx in possible_end_idx:
                val.append([st_idx -1, end_idx -1, dif[st_idx:end_idx].sum()])

        df_val = pd.DataFrame(val, columns = ('st_idx', 'end_idx', 'increase'))
        max_increase_idx = df_val.increase.idxmax()
        st_idx, end_idx, max_increase = df_val.iloc[max_increase_idx,0], df_val.iloc[max_increase_idx,1], df_val.iloc[max_increase_idx,2]
        max_increase_ratio = max_increase/df.iloc[st_idx,CLOSE]
        st_date, end_date = df.iloc[st_idx,:].date, df.iloc[end_idx,:].date
        return {
            'start_date': st_date,
            'end_date': end_date,
            'max_increase': max_increase,
            'max_increase_ratio': max_increase_ratio,
        }
    
    def calc_year_increase(self, target_date):
        if ~isinstance(target_date, datetime):
            target_date = datetime.strptime(target_date, '%Y-%m-%d')
        for i in range(10):
            target = self.annual_data[self.annual_data.date == target_date]
            if len(target) == 0:
                target_date -= timedelta(days = i)
            else:
                target_close = target.close.values[0]
                break
        year_increase = target_close - self.first_working_close
        year_increase_ratio = year_increase / self.first_working_close
        return {
            'target_date': target_date,
            'target_close': target_close,
            'year_increase': year_increase,
            'year_increase_ratio': year_increase_ratio,
        }