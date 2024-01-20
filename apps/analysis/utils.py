import pandas as pd
import numpy as np

def calDailyReturns(data=pd.DataFrame()):
    """ 
        this def accept one parameter data of datatype DataFrame and calculate daily returns for the same :
            params :
                    data (DataFrame): historical data of symbol like  nifty50 containing columns (date,open,high,low,close,sharestraded,turnover) 

            returns dataframe containing date and dailyreturns column
    """
    # converting column names to lowercase and removing space form start and end
    rename_cols = { i:i.strip().lower() for i in data.columns }
    data.rename(columns=rename_cols,inplace=True)
    
    # converting date column to datatype date and sorting it in ascending based on date
    data['date'] = pd.to_datetime(data['date'])    
    data.sort_values(by='date',inplace=True)

    # calculating dailyreturn and returning them
    data['dailyreturns'] = (data['close']/data['close'].shift(1))-1
    return data[['date','dailyreturns']]


def calDailyVolatility(data=pd.DataFrame()):
    """ 
        this def calculates daily volatility based on daily reutunrs
    """
    return (data['dailyreturns'].std())


def calAnnualizedVolatility(dailyreturns=0,lenthOfData=0):
    """ 
        this def calculates annual volatility 
        params : 
                dailyreturn : daily returns calculated (float)
                lengthofdata : lendth of the data in file uploaded
    """
    return dailyreturns*(np.sqrt(lenthOfData))



