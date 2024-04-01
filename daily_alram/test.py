from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import FinanceDataReader as fdr
import yfinance as yf

# pandas 설정: 최대 행, 열 출력 설정
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def get_stock_data_and_info(ticker, start_date, end_date):
    data = fdr.DataReader(ticker, start=start_date, end=end_date)
    return data

def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

today = datetime.now()
start_date = (today - timedelta(days=10)).strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')

ticker = 'KS11'
ticker_y = '^KS11'

kospi_data_df = get_stock_data_and_info(ticker, start_date, end_date)
kospi_data_df_y = get_stock_data(ticker_y, start_date, end_date)
print(kospi_data_df)
print(kospi_data_df_y)