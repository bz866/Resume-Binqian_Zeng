'''
Created on Feb 23, 2020

@author: Binqian Zeng, Binlin Chi, Xuan Zhang

The script contains a class as the solution of HW1 PartB.1 to compute X-minute
returns of trades and mid-quotes, where X is arbitrary

'''

import pandas as pd
import numpy as np
import datetime

class CalculatorOfReturns:
    '''
    compute X-minute returns of trades and mid-quotes, where X is arbitrary
    - For simplicity, X is integer.
    - Interval of return is arbitrary and specified by users
    '''


    def __init__(self, nameOfCompany: str, X: int, baseDirectory: str='./') -> None:
        '''
        Constructor
        @param nameOfCompany: trading symbol of a company, e.g. TEL, A, ...
        @param baseDirectory: the path of the directory that contains folders of quotes and trades
        @param X: the integer X-minutes time interval
        '''
        self._nameOfCompany = nameOfCompany
        self._baseDirectory = baseDirectory
        self._timeInterval = X
        self._dfTrades = pd.read_csv(self._baseDirectory + '/trades_SP500/' + self._nameOfCompany + '_trades.csv')
        self._dfQuotes = pd.read_csv(self._baseDirectory + 'quotes_SP500/' + self._nameOfCompany + '_quotes.csv')
        self._dfTrades.drop_duplicates(inplace=True)
        self._dfQuotes.drop_duplicates(inplace=True)
        # convert date and millisec as datetime timestamp
        self._dfTrades['timestamp'] = pd.datetime(self._dfTrades['rqie '].astype(str)) + self._dfTrades['millisec_mid'].apply(lambda x: datetime.timedelta(milliseconds=x))
        self._dfQuotes['timestamp'] = pd.datetime(self._dfQuotes['rqie '].astype(str)) + self._dfQuotes['millisec_mid'].apply(lambda x: datetime.timedelta(milliseconds=x))
        
    def computeReturnsOfTrade(self) -> pd.DataFrame:
        '''
        Compute X-minute returns of trades of a specific company
        If X-minute interval record is not available,  rounding of time interval to find nearest X minutes return. 
        
        @return: the dataframe with columns ['rqie ', 'millisec_mid_start', 'millisec_mid_end', 'millisec_mid_end_nearest', 'trade_price_first', 'trade_price_last']
        'millisec_mid_end' = 'millisec_mid_start' + X * 60000 millisec
        'millisec_mid_end_nearest' is the closest millisec with trading record
        '''
        dfReturnsOfTrade = self._dfTrades.copy()
        dfReturnsOfTrade.drop(labels=['trade_size'], axis=1, inplace=True) # drop unnecessary column
        # convert the datetime and millisec as time stamp to search the closest time stamp with given time interval
        dfReturnsOfTrade['rqie '] = dfReturnsOfTrade['rqie'].apply(lambda x: pd.to_datetime(x),  "%Y-%m-%d")
        dfReturnsOfTrade['millisec_mid_timedelta'] = dfReturnsOfTrade['millisec_mid'].apply(lambda x: datetime.timedelta(milliseconds=x))
        dfReturnsOfTrade['timestamp'] = dfReturnsOfTrade['rqie '] + dfReturnsOfTrade['millisec_mid_timedelta'] 
        dfReturnsOfTrade.set_index(keys=['timestamp'], inplace=True)
        # drop duplicate trading records for fast search nearest time stamp using pandas
#         dfReturnsOfTrade.drop_duplicates(inplace=True)
        dfReturnsOfTrade= dfReturnsOfTrade.loc[~dfReturnsOfTrade.index.duplicate(keep='first')].index
        dfReturnsOfTrade['timestampWithInterval'] = dfReturnsOfTrade.index - self._timeInterval * datetime.timedelta(milliseconds=60000) # 1 mins = 60000 milliseconds
        # find the nearest time stamp with trading records
        res = dfReturnsOfTrade['timestampWithInterval'].apply(lambda x: dfReturnsOfTrade.iloc[dfReturnsOfTrade.index.get_loc(x, method='nearest')][['trade_price', 'rqie ', 'millisec_mid_timedelta']])
        dfReturnsOfTrade['cloest_timestamp'] = res['rqie '] + res['millisec_mid_timedelta']
        dfReturnsOfTrade['trade_price_first'] = res['trade_price']
        dfReturnsOfTrade.rename(columns={'trade_price': 'trade_price_last'}, inplace=True)
        # calculate the return of trades
        dfReturnsOfTrade['return_of_trade'] = (dfReturnsOfTrade['trade_price_last'] - dfReturnsOfTrade['trade_of_first']) / dfReturnsOfTrade['trade_of_first']
        # drop unnecessary columns
        dfReturnsOfTrade = dfReturnsOfTrade[['rqie ', 'millisec_mid', 'millisec_mid_timedelta', 'trade_price_first', 'trade_price_last', 'cloest_timestamp', 'return_of_trade']]
        dfReturnsOfTrade.reset_index()
        
        return dfReturnsOfTrade
    
    def computeMidQuotes(self) -> pd.DataFrame:
        '''
        Compute X-minute return of mid-quotes of a specific company
        The mid-quote is defined as average between the lowest ask price and the highest bid price of a tick
        If X-minute interval record is not available,  rounding of time interval to find nearest X minutes return. 
        '''
        
        return
        
    # Getters
    def getNameOfCompany(self) -> str:
        return self._nameOfCompany
    
    def getTradesAsDF(self) -> pd.DataFrame:
        return self._dfTrades
    
    def getQuotesAsDF(self) -> pd.DataFrame:
        return self._dfQuotes
    
    def getTimeInterval(self) -> int:
        return self._timeInterval
    
    # Setters
    def setNameOfCompany(self, newNameOfCompany: str) -> None:
        self._nameOfCompany = newNameOfCompany
        # read the trades and quotes records of the new company
        self._dfTrades = pd.read_csv(self._baseDirectory + '/trades/' + self._nameOfCompany + '_trades.csv')
        self._dfQuotes = pd.read_csv(self._baseDirectory + 'quotes/' + self._nameOfCompany + '_quotes.csv')
        
    def setTimeInterval(self, newTimeInterval: int) -> None:
        self._timeInterval = newTimeInterval
        
    
    
    
    
        