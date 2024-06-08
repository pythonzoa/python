import pandas as pd
import FinanceDataReader as fdr
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 경로 설정
font_path = 'C:\\Windows\\Fonts\\malgun.ttf'  # 한글 폰트의 경로를 지정합니다.

# 한글 폰트 설정
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

# 주식 데이터를 가져오는 함수 정의
def fetch_stock_data(stock_code, start_date):
    try:
        end_date = start_date + timedelta(days=180)  # 시작 날짜로부터 6개월 후
        df_stock = fdr.DataReader(stock_code, start_date, end_date)
        return df_stock
    except Exception as e:
        print(f"{stock_code} 데이터를 가져오는 중 오류 발생: {e}")
        return None

# 주식 차트를 저장하는 함수
# 주식 차트를 저장하는 함수
def save_stock_chart(df_stock, stock_code, start_date, stock_name):
    if df_stock is not None and not df_stock.empty:
        plt.figure(figsize=(10, 6))
        plt.plot(df_stock.index, df_stock['Close'], label='종가')

        # 평균 주가를 가로선으로 추가
        mean_price = df_stock['Close'].mean()
        plt.axhline(y=mean_price, color='r', linestyle='--', label='평균 주가')

        # 첫날 종가를 회색 수평선으로 추가
        first_day_close_price = df_stock.iloc[0]['Close']
        plt.axhline(y=first_day_close_price, color='gray', linestyle='--', label='첫날 종가')

        plt.title(f'{stock_name}의 {start_date.strftime("%Y-%m-%d")}부터의 주가 추이')
        plt.xlabel('날짜')
        plt.ylabel('종가')
        plt.legend()
        safe_start_date = start_date.strftime("%Y-%m-%d").replace(":", "-").replace(" ", "_")
        plt.savefig(f'{stock_name}_{safe_start_date}.png')
        plt.close()
        print(f"{stock_name} 차트 저장 완료")
    else:
        print(f"{stock_code} 데이터가 없어 차트를 그릴 수 없습니다.")


# Excel 파일에서 주식 코드를 로드
file_path = r'C:\Users\TMS\Downloads\gogogo.xlsx'  # 파일 경로 업데이트 필요
df_names = pd.read_excel(file_path, sheet_name='names')
# 'stock_code' 열의 값이 숫자로 변환 가능한지 확인 후 변환, 아니면 NaN 할당
df_names['stock_code'] = pd.to_numeric(df_names['stock_code'], errors='coerce')
# NaN 값을 포함한 행 제거
df_names = df_names.dropna(subset=['stock_code'])
# stock_code를 문자열로 변환하고 형식에 맞게 포맷팅
df_names['stock_code'] = df_names['stock_code'].apply(lambda x: str(int(x)).zfill(6))

# 각 주식에 대해 데이터를 가져오고 차트를 저장
for index, row in df_names.iterrows():
    stock_code = row['stock_code']
    stock_name = row['stock_name']
    start_date = pd.to_datetime(row['ekbun_date'])
    df_stock = fetch_stock_data(stock_code, start_date)
    save_stock_chart(df_stock, stock_code, start_date, stock_name)
