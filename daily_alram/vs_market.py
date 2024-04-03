import FinanceDataReader as fdr
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import pandas as pd
import datetime
import os
from daily_alram import sichong

# 한글 폰트 및 음수 부호 설정
font_path = 'C:\\Windows\\Fonts\\malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False

# 최상위 폴더 생성
end_date = datetime.datetime.today()
top_folder_name = end_date.strftime('%Y-%m-%d_%H-%M-%S')
top_folder_path = os.path.join(os.getcwd(), top_folder_name)
os.makedirs(top_folder_path, exist_ok=True)

def main(start_days_ago):
    # 하위 폴더 생성
    sub_folder_name = f"days_{start_days_ago}"
    new_folder_path = os.path.join(top_folder_path, sub_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)

    # 코스피 및 코스닥 하위 폴더 생성
    kospi_folder_path = os.path.join(new_folder_path, "KOSPI")
    kosdaq_folder_path = os.path.join(new_folder_path, "KOSDAQ")
    os.makedirs(kospi_folder_path, exist_ok=True)
    os.makedirs(kosdaq_folder_path, exist_ok=True)

    # 20거래일 전 날짜 계산
    recent_market_data = fdr.DataReader('KS11', end_date - datetime.timedelta(days=120), end_date)
    trading_days = recent_market_data.index
    if len(trading_days) >= start_days_ago:
        twentieth_trading_day = trading_days[-start_days_ago]
    else:
        twentieth_trading_day = trading_days[0]
    start_date = twentieth_trading_day

    # 코스피 및 코스닥 지수 데이터
    kospi_index = fdr.DataReader('KS11', start_date, end_date)['Close'].pct_change().fillna(0).add(1).cumprod().sub(1)
    kosdaq_index = fdr.DataReader('KQ11', start_date, end_date)['Close'].pct_change().fillna(0).add(1).cumprod().sub(1)

    def plot_stock_with_index(stock_symbol, index_data, stock_name, index_name, category, sub_folder_path):
        stock_data = fdr.DataReader(stock_symbol, start_date, end_date)
        stock_cumulative_return = stock_data['Close'].pct_change().fillna(0).add(1).cumprod().sub(1)

        plt.figure(figsize=(12, 6))
        plt.plot(stock_data.index, stock_cumulative_return, label=f"{stock_name}", color='red')
        plt.plot(index_data.index, index_data, label=f"{index_name}", color='gray', linestyle='-.')
        plt.title(f'{stock_name} vs. {index_name}')
        plt.xlabel('일시')
        plt.ylabel('누적수익률')
        plt.legend()
        plt.savefig(os.path.join(sub_folder_path, f"{category}_{stock_name}.png"))
        plt.close()

    kospiStocks = sichong.kospi_stocks_by_rate
    kosdaqStocks = sichong.kosdaq_stocks_by_rate

    def update_with_intersection(stocks_dict):
        daily_gain_rate_stocks = set(stocks_dict['Daily_Gain_Rate'])
        thirty_days_gain_rate_stocks = set(stocks_dict['30days_Gain_Rate'])
        intersection_stocks = daily_gain_rate_stocks.intersection(thirty_days_gain_rate_stocks)

        new_dict = {'30days_Gain_Rate': list(intersection_stocks)}
        return new_dict

    kospi_stocks = update_with_intersection(kospiStocks)
    kosdaq_stocks = update_with_intersection(kosdaqStocks)

    for category, stocks in kospi_stocks.items():
        for name, symbol in stocks:
            plot_stock_with_index(symbol, kospi_index, name, "KOSPI", category, kospi_folder_path)

    for category, stocks in kosdaq_stocks.items():
        for name, symbol in stocks:
            plot_stock_with_index(symbol, kosdaq_index, name, "KOSDAQ", category, kosdaq_folder_path)

main(21)
