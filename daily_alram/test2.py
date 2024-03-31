import FinanceDataReader as fdr
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import datetime
import os
from daily_alram import sichong

# 한글 폰트 및 음수 부호 설정
font_path = 'C:\\Windows\\Fonts\\malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False

def main(start_days_ago):
    # 오늘 날짜 및 계산된 시작 날짜
    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=start_days_ago)

    # 폴더 생성
    folder_name = f"{end_date.strftime('%Y-%m-%d_%H-%M-%S')}"
    new_folder_path = os.path.join(os.getcwd(), folder_name)
    os.makedirs(new_folder_path, exist_ok=True)

    # 코스피 및 코스닥 지수 데이터
    kospi_index = fdr.DataReader('KS11', start_date, end_date)['Close'].pct_change().fillna(0).add(1).cumprod().sub(1)
    kosdaq_index = fdr.DataReader('KQ11', start_date, end_date)['Close'].pct_change().fillna(0).add(1).cumprod().sub(1)

    # 주식 및 지수 시각화 함수 정의
    def plot_stock_with_index(stock_symbol, index_data, stock_name, index_name, category):
        stock_data = fdr.DataReader(stock_symbol, start_date, end_date)
        stock_cumulative_return = stock_data['Close'].pct_change().fillna(0).add(1).cumprod().sub(1)

        plt.figure(figsize=(14, 7))
        plt.plot(stock_data.index, stock_cumulative_return, label=f"{stock_name}", color='red')
        plt.plot(index_data.index, index_data, label=f"{index_name}", color='gray', linestyle='-.')
        plt.title(f'{category} 누적 상승률 of {stock_name} vs. {index_name}')
        plt.xlabel('일시')
        plt.ylabel('누적수익률(%)')
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
main(32)
main(90)
