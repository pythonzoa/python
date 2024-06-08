import pandas as pd
import FinanceDataReader as fdr
from datetime import timedelta
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 경로 설정
font_path = 'C:\\Windows\\Fonts\\malgun.ttf'  # 한글 폰트의 경로입니다.
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

def fetch_stock_data(stock_code, start_date):
    """
    주어진 주식 코드와 시작 날짜에 따라 주식 데이터를 가져오는 함수입니다.
    시작 날짜로부터 180일(약 6개월) 후까지의 데이터를 가져옵니다.
    """
    try:
        end_date = start_date + timedelta(days=180)
        df_stock = fdr.DataReader(stock_code, start_date, end_date)
        if df_stock.empty:
            print(f"{stock_code}에 대한 데이터가 없습니다. 데이터를 건너뜁니다.")
            return None
        return df_stock
    except Exception as e:
        print(f"{stock_code} 데이터를 가져오는 중 오류 발생: {e}")
        return None

# 초기 DataFrame 생성
df_all_summaries = pd.DataFrame(columns=['종목코드', '종목명', '기간 내 최고종가', '기간 내 최저종가', '첫날 종가 대비 최고종가 수익률(%)', '첫날 종가 대비 최저종가 수익률(%)'])

def calculate_and_append_data(df_stock, stock_code, stock_name, start_date):
    """
    주식 데이터를 분석하여 요약 정보를 계산하고, 이를 요약 정보 DataFrame에 추가하는 함수입니다.
    """
    global df_all_summaries
    if df_stock is not None and not df_stock.empty:
        highest_close = df_stock['Close'].max()
        lowest_close = df_stock['Close'].min()
        first_day_close = df_stock.iloc[0]['Close']
        highest_return = ((highest_close - first_day_close) / first_day_close) * 100
        lowest_return = ((lowest_close - first_day_close) / first_day_close) * 100

        df_new_summary = pd.DataFrame({
            '종목코드': [stock_code],
            '종목명': [stock_name],
            '기간 내 최고종가': [highest_close],
            '기간 내 최저종가': [lowest_close],
            '첫날 종가 대비 최고종가 수익률(%)': [highest_return],
            '첫날 종가 대비 최저종가 수익률(%)': [lowest_return]
        })
        if not df_new_summary.empty:
            df_all_summaries = pd.concat([df_all_summaries, df_new_summary], ignore_index=True)

    else:
        print(f"{stock_code}에 대한 분석 데이터가 없습니다.")

# Excel 파일에서 주식 코드 로드
file_path = r'C:\Users\TMS\Downloads\gogogo.xlsx'
df_names = pd.read_excel(file_path, sheet_name='names')
df_names['stock_code'] = pd.to_numeric(df_names['stock_code'], errors='coerce').dropna().apply(lambda x: str(int(x)).zfill(6))

for index, row in df_names.iterrows():
    stock_code = row['stock_code']
    stock_name = row['stock_name']
    start_date = pd.to_datetime(row['ekbun_date'])
    df_stock = fetch_stock_data(stock_code, start_date)
    if df_stock is not None and not df_stock.empty:
        calculate_and_append_data(df_stock, stock_code, stock_name, start_date)
    else:
        print(f"{stock_code} ({stock_name})에 대한 데이터가 충분하지 않습니다.")

# 모든 데이터 처리 후 Excel 파일로 저장
excel_path = 'all_stocks_summary.xlsx'
df_all_summaries.to_excel(excel_path, index=False)
print(f"{excel_path}에 모든 주식 데이터 요약 정보가 저장되었습니다.")
