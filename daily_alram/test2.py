from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import yfinance as yf

# pandas 설정: 최대 행, 열 출력 설정
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def calculate_weekly_last_close_with_last_month(df):
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("DataFrame 인덱스는 DatetimeIndex 타입이어야 합니다.")

    # 주차 및 월 정보 추출
    df['Week_Num'] = df.index.isocalendar().week
    df['Month_Num'] = df.index.month

    # 주차별 및 월별 마지막 거래일 정보 추출
    last_weekly_close = df.groupby('Week_Num').tail(1)
    last_monthly_close = df.groupby('Month_Num').tail(1)

    # 각 마지막 거래일 정보 저장을 위한 임시 DataFrame 생성
    temp_df = pd.DataFrame({
        'Date': last_weekly_close.index,
        'Last_Week_Close': last_weekly_close['Close'],
        'Last_Week_Close_Date': last_weekly_close.index
    }).set_index('Date')

    # 임시 DataFrame 정보를 원본 DataFrame에 매핑
    df = df.join(temp_df[['Last_Week_Close', 'Last_Week_Close_Date']], on=df.index, how='left')
    df[['Last_Week_Close', 'Last_Week_Close_Date']] = df[['Last_Week_Close', 'Last_Week_Close_Date']].ffill()

    # Year_Month 컬럼 추가
    df['Year_Month'] = df.index.to_period('M')

    # 직전 달의 마지막 거래일 종가 및 날짜 매핑
    monthly_close_mapping = last_monthly_close.groupby('Month_Num')['Close'].last()
    # 월별 마지막 거래일 날짜 매핑 수정
    monthly_dates_mapping = df.groupby('Month_Num')['Year_Month'].max().apply(lambda x: x.end_time.date()).to_dict()

    df['Last_Month_Close'] = df['Month_Num'].apply(lambda x: x - 1 if x > 1 else 12).map(monthly_close_mapping)
    df['Last_Month_Close_Date'] = df['Month_Num'].apply(lambda x: x - 1 if x > 1 else 12).map(monthly_dates_mapping)

    # 불필요한 컬럼 제거
    df.drop(['Week_Num', 'Month_Num', 'Year_Month'], axis=1, inplace=True)

    df['Last_Week_Close'] = df['Last_Week_Close'].shift(1)
    df['Last_Week_Close_Date'] = df['Last_Week_Close_Date'].shift(1)

    return df


# 주가 데이터 추출 함수
def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def add_additional_columns(df):
    # 현재 주차 ('this_week')
    df['this_week'] = df.index.isocalendar().week

    # 직전 주차 ('last_week')
    df['last_week'] = df['this_week'] - 1

    # 지난달 ('last_month')
    df['last_month'] = df.index.month - 1
    df.loc[df['last_month'] == 0, 'last_month'] = 12

    # 20거래일 전 날짜 ('30days') 및 종가 ('30days_Close')
    df['30days'] = df['key_0'].shift(20)
    df['30days_Close'] = df['Close'].shift(20)

    # 60거래일 전 날짜 ('90days') 및 종가 ('90days_Close')
    df['90days'] = df['key_0'].shift(60)
    df['90days_Close'] = df['Close'].shift(60)

    # 상승률 계산
    df['Monthly_Gain_Rate'] = (df['Close'] - df['Last_Month_Close']) / df['Last_Month_Close'] * 100
    df['30days_Gain_Rate'] = (df['Close'] - df['30days_Close']) / df['30days_Close'] * 100
    df['90days_Gain_Rate'] = (df['Close'] - df['90days_Close']) / df['90days_Close'] * 100

    return df


# 사용 예시
kospi_ticker = '^KS11'
kosdaq_ticker = '^KQ11'
today = datetime.now()
start_date = (today - timedelta(days=100)).strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')

kospi_data_df = get_stock_data(kospi_ticker, start_date, end_date)
kosdaq_data_df = get_stock_data(kosdaq_ticker, start_date, end_date)

# DataFrame에 필요한 처리 적용
kospi_data_df = calculate_weekly_last_close_with_last_month(kospi_data_df)
kosdaq_data_df = calculate_weekly_last_close_with_last_month(kosdaq_data_df)

# 필요한 데이터만 추출 및 전일 종가 추가
kospi_data_df = kospi_data_df[['Open', 'Close']].copy()
kosdaq_data_df = kosdaq_data_df[['Open', 'Close']].copy()
kospi_data_df['Prev_Close'] = kospi_data_df['Close'].shift(1)
kosdaq_data_df['Prev_Close'] = kosdaq_data_df['Close'].shift(1)

# KOSPI와 KOSDAQ 데이터에 주차별 마지막 거래일 종가 계산 적용
kospi_data_df = calculate_weekly_last_close_with_last_month(kospi_data_df)
kosdaq_data_df = calculate_weekly_last_close_with_last_month(kosdaq_data_df)

# 전일 대비 상승률 및 직전주 마지막 거래일 대비 상승률 계산
kospi_data_df['Daily_Gain_Rate'] = (kospi_data_df['Close'] - kospi_data_df['Prev_Close']) / kospi_data_df['Prev_Close'] * 100
kosdaq_data_df['Daily_Gain_Rate'] = (kosdaq_data_df['Close'] - kosdaq_data_df['Prev_Close']) / kosdaq_data_df['Prev_Close'] * 100
kospi_data_df['Weekly_Gain_Rate'] = (kospi_data_df['Close'] - kospi_data_df['Last_Week_Close']) / kospi_data_df['Last_Week_Close'] * 100
kosdaq_data_df['Weekly_Gain_Rate'] = (kosdaq_data_df['Close'] - kosdaq_data_df['Last_Week_Close']) / kosdaq_data_df['Last_Week_Close'] * 100
def reorder_columns(df):
    columns_order = [
        'key_0', 'Close', 'Daily_Gain_Rate', 'Last_Week_Close_Date', 'Last_Week_Close',
        'Weekly_Gain_Rate', 'Last_Month_Close_Date', 'Last_Month_Close', 'Monthly_Gain_Rate',
        '30days', '30days_Close', '30days_Gain_Rate', '90days', '90days_Close', '90days_Gain_Rate'
    ]
    # 'key_0' 컬럼이 실제 데이터에 없을 경우를 대비한 검사 포함
    final_columns = [col for col in columns_order if col in df.columns]
    return df[final_columns]

# 함수 적용
kospi_data_df = add_additional_columns(kospi_data_df)
kospi_data_df = reorder_columns(kospi_data_df)

kosdaq_data_df = add_additional_columns(kosdaq_data_df)
kosdaq_data_df = reorder_columns(kosdaq_data_df)


print("코스피 데이터:")
print(kospi_data_df.tail())

print("\n코스닥 데이터:")
print(kosdaq_data_df.tail())
