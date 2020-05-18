#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 12:16:52 2020

@author: kelly
"""
from simple_port import *
import datetime as dt 


if __name__=='__main__': 
    
    tickers = ['GOOGL', 'NEE','AMD','KO']
    start = dt.datetime(2019,1,1)
    end = dt.datetime(2019,12,31)
    port = portfolio(4, 10000,tickers,start,end, 0)
#    print(port.sp500)
    df,max_sharpe_port = port.Find_Sharpe_Ratio()
    print(df)
    print(" num of NaN in port_risk:",df['port_risk'].isnull().sum(axis = 0))
    print("average return of all portfolio: ", df['expected_return'].mean())
    print("SP500 return:", port.sp500)
    print("the portfolio with maximal sharpe ratio:\n", max_sharpe_port)    
    
    