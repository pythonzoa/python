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

    # 20거래일 전 날짜 계산
    recent_market_data = fdr.DataReader('KS11', end_date - datetime.timedelta(days=120),end_date)  # 충분히 거슬러 올라가서 데이터를 가져옵니다.
    trading_days = recent_market_data.index  # 거래일 인덱스를 가져옵니다.
    if len(trading_days) >= start_days_ago:
        twentieth_trading_day = trading_days[-start_days_ago]
    else:
        # 길이가 부족한 경우, 가능한 가장 이른 날짜 사용
        twentieth_trading_day = trading_days[0]
    start_date = twentieth_trading_day  # 시작 날짜를 설정합니다.


    # 코스피 및 코스닥 지수 데이터
    kospi_index = fdr.DataReader('KS11', start_date, end_date)['Close'].pct_change().fillna(0).add(1).cumprod().sub(1)
    kosdaq_index = fdr.DataReader('KQ11', start_date, end_date)['Close'].pct_change().fillna(0).add(1).cumprod().sub(1)

    # 주식 및 지수 시각화 함수 정의
    def plot_stock_with_index(stock_symbol, index_data, stock_name, index_name, category):
        stock_data = fdr.DataReader(stock_symbol, start_date, end_date)
        stock_cumulative_return = stock_data['Close'].pct_change().fillna(0).add(1).cumprod().sub(1)

        plt.figure(figsize=(12, 6))
        plt.plot(stock_data.index, stock_cumulative_return, label=f"{stock_name}", color='red')
        plt.plot(index_data.index, index_data, label=f"{index_name}", color='gray', linestyle='-.')
        plt.title(f'{stock_name} vs. {index_name}')
        plt.xlabel('일시')
        plt.ylabel('누적수익률')
        plt.legend()
        plt.savefig(os.path.join(new_folder_path, f"{category}_{stock_name}.png"))
        plt.close()

    # 코스피 및 코스닥 종목 시각화
    kospi_stocks = sichong.kospi_stocks_by_rate
    kosdaq_stocks = sichong.kosdaq_stocks_by_rate

    for category, stocks in kospi_stocks.items():
        for name, symbol in stocks:
            plot_stock_with_index(symbol, kospi_index, name, "KOSPI", category)

    for category, stocks in kosdaq_stocks.items():
        for name, symbol in stocks:
            plot_stock_with_index(symbol, kosdaq_index, name, "KOSDAQ", category)


# 30일과 90일 기간에 대해 메인 함수 실행
main(21)
