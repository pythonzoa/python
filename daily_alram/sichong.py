from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import FinanceDataReader as fdr
from daily_alram import strongstock

# pandas 설정: 최대 행, 열 출력 설정
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

kospiData = strongstock.kospi_data_df
kosdaqData = strongstock.kosdaq_data_df

## KRX 상장 회사 목록을 불러옴
krx_list = fdr.StockListing('KRX')

# 시가총액 기준 필터링 조건 적용
kospi_tickers = krx_list[(krx_list['Market'] == 'KOSPI') & (krx_list['Marcap'] >= 5e12)]['Code'].tolist()
kosdaq_tickers = krx_list[(krx_list['Market'] == 'KOSDAQ') & (krx_list['Marcap'] >= 1e12)]['Code'].tolist()


# 특정 티커에 대한 주가 데이터와 회사 정보를 가져오는 함수
def get_stock_data_and_info(ticker, start_date, end_date):
    data = fdr.DataReader(ticker, start=start_date, end=end_date)
    info = krx_list[krx_list['Code'] == ticker].iloc[0]
    return data, info['Name'], info['Market'], info['Marcap']


today = datetime.now()
start_date = (today - timedelta(days=100)).strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')


# 데이터프레임에 회사 정보를 추가하는 함수
def add_company_info(df, ticker):
    _, name, market, marcap = get_stock_data_and_info(ticker, start_date, end_date)
    df['Name'] = name
    df['Market'] = market
    df['Marcap'] = marcap
    return df


# 데이터 다운로드 및 정보 추가
kospi_data_dfs = {ticker: add_company_info(fdr.DataReader(ticker, start_date, end_date), ticker) for ticker in
                  kospi_tickers}
kosdaq_data_dfs = {ticker: add_company_info(fdr.DataReader(ticker, start_date, end_date), ticker) for ticker in
                   kosdaq_tickers}


def process_market_data(data_dfs):
    new_column_order = [
        'key_0','Close', 'Prev_Close', 'Daily_Gain_Rate', 'Last_Week_Close_Date', 'Last_Week_Close',
        'Weekly_Gain_Rate', 'Last_Month_Close_Date', 'Last_Month_Close', 'Monthly_Gain_Rate',
        '30days', '30days_Close', '30days_Gain_Rate', '90days', '90days_Close', '90days_Gain_Rate',
        'Name', 'Market', 'Marcap'
    ]

    for key in data_dfs.keys():
        df = data_dfs[key]
        df['Close'] = df['Close'].astype(float)
        df = df[['Close', 'Name', 'Market', 'Marcap']].copy()
        df['Prev_Close'] = df['Close'].shift(1)
        df['Week_Num'] = df.index.isocalendar().week
        df['Month_Num'] = df.index.month
        df['Year'] = df.index.isocalendar().year
        max_week_by_year = df.groupby('Year')['Week_Num'].max().to_dict()

        # 주차별로 그룹화하여 각 주차별 마지막 거래일의 종가를 계산
        df['Last_Week_Close_Temp'] = df.groupby('Week_Num')['Close'].transform('last')
        # 전년도 최대 주차 번호를 고려하여 Week_Num_Plus_One 계산
        def calculate_previous_week(row):
            if row['Week_Num'] == 1:
                # 현재 주차가 1주차인 경우, 전년도의 최대 주차 번호 사용
                previous_year = row['Year'] - 1
                return max_week_by_year.get(previous_year, 52)  # 전년도 정보가 없으면 기본값으로 52 사용
            else:
                # 그 외의 경우, 현재 주차에서 1을 빼서 반환
                return row['Week_Num'] - 1
        df['Week_Num_Plus_One'] = df.apply(calculate_previous_week, axis=1)

        # 주차 번호와 일치하는 주차의 마지막 거래일 종가를 매핑
        df['Last_Week_Close'] = df['Week_Num_Plus_One'].map(df.groupby('Week_Num')['Last_Week_Close_Temp'].last())
        df.drop(['Last_Week_Close_Temp', 'Week_Num_Plus_One'], axis=1, inplace=True)

        # 월별로 그룹화하여 각 월별 마지막 거래일의 종가를 계산
        df['Last_Month_Close_Temp'] = df.groupby('Month_Num')['Close'].transform('last')
        # Month_Num 컬럼을 활용하여 다음 달을 표시하는 새로운 컬럼을 생성
        df['Next_Month_Num'] = df['Month_Num'] - 1
        df.loc[df['Next_Month_Num'] == 0, 'Next_Month_Num'] = 12
        df['Last_Month_Close'] = df['Next_Month_Num'].map(df.groupby('Month_Num')['Last_Month_Close_Temp'].last())

        # 필요 없는 임시 컬럼 삭제
        df.drop(['Last_Month_Close_Temp', 'Next_Month_Num'], axis=1, inplace=True)

        df['Daily_Gain_Rate'] = (df['Close'] - df['Prev_Close']) / df['Prev_Close'] * 100
        df['Weekly_Gain_Rate'] = (df['Close'] - df['Last_Week_Close']) / df['Last_Week_Close'] * 100
        df['Monthly_Gain_Rate'] = (df['Close'] - df['Last_Month_Close']) / df['Last_Month_Close'] * 100

        # 20거래일 전 날짜 ('30days') 및 종가 ('30days_Close')
        # df['30days'] = df['key_0'].shift(20)
        df['30days_Close'] = df['Close'].shift(20)

        # 60거래일 전 날짜 ('90days') 및 종가 ('90days_Close')
        # df['90days'] = df['key_0'].shift(60)
        df['90days_Close'] = df['Close'].shift(60)

        # 상승률 계산
        df['30days_Gain_Rate'] = (df['Close'] - df['30days_Close']) / df['30days_Close'] * 100
        df['90days_Gain_Rate'] = (df['Close'] - df['90days_Close']) / df['90days_Close'] * 100

        # 새로운 컬럼 순서로 DataFrame 재정렬
        df = df.reindex(columns=new_column_order)

        # 기타 필요한 계산 및 컬럼 재정렬
        # df = df.reindex(columns=new_column_order) # 필요한 경우 컬럼 순서를 재정렬할 수 있습니다.
        data_dfs[key] = df

    return data_dfs

# kospi_data_dfs와 kosdaq_data_dfs에 대해 함수 적용하고 결과 DataFrame 받기
kospi_final_df = process_market_data(kospi_data_dfs)
kosdaq_final_df = process_market_data(kosdaq_data_dfs)

def combine_last_rows(data_dfs):
    # 각 데이터프레임의 마지막 행만 선택하여 새로운 리스트에 저장
    last_rows_list = [df.iloc[[-1]].assign(Ticker=key) for key, df in data_dfs.items()]
    # 리스트에 저장된 데이터프레임들을 하나로 결합
    combined_df = pd.concat(last_rows_list, ignore_index=True)
    return combined_df

# KOSPI 데이터프레임들에 대해 마지막 행을 결합
combined_kospi_df = combine_last_rows(kospi_data_dfs)
# KOSDAQ 데이터프레임들에 대해 마지막 행을 결합
combined_kosdaq_df = combine_last_rows(kosdaq_data_dfs)

# kospiData와 combined_kospi_df의 컬럼 중 일치하는 컬럼만 찾기
matching_columns = kospiData.columns.intersection(combined_kospi_df.columns)
matching_columnsQ = kosdaqData.columns.intersection(combined_kosdaq_df.columns)

# kospiData의 마지막 행에서 일치하는 컬럼에 해당하는 값만 추출
last_row_selected_columns = kospiData[matching_columns].iloc[-1:]
last_row_selected_columnsQ = kosdaqData[matching_columns].iloc[-1:]

# combined_kospi_df가 비어 있는지 확인
if combined_kospi_df.empty:
    print("combined_kospi_df는 비어 있습니다.")
else:
    # 모두 NA 값으로만 구성된 열을 제거
    combined_kospi_df = combined_kospi_df.dropna(axis=1, how='all')

# last_row_selected_columns가 비어 있는지 확인
if last_row_selected_columns.empty:
    print("last_row_selected_columns는 비어 있습니다.")
else:
    # 모두 NA 값으로만 구성된 열을 제거
    non_na_columns = last_row_selected_columns.dropna(axis=1, how='all').columns
    filtered_last_row_selected_columns = last_row_selected_columns[non_na_columns]
    # 정제된 데이터프레임 결합
    combined_kospi_df = pd.concat([combined_kospi_df, filtered_last_row_selected_columns], ignore_index=True)

# combined_kosdaq_df와 last_row_selected_columnsQ에 대해서도 동일한 과정 수행
if combined_kosdaq_df.empty:
    print("combined_kosdaq_df는 비어 있습니다.")
else:
    combined_kosdaq_df = combined_kosdaq_df.dropna(axis=1, how='all')

if last_row_selected_columnsQ.empty:
    print("last_row_selected_columnsQ는 비어 있습니다.")
else:
    non_na_columnsQ = last_row_selected_columnsQ.dropna(axis=1, how='all').columns
    filtered_last_row_selected_columnsQ = last_row_selected_columnsQ[non_na_columnsQ]
    combined_kosdaq_df = pd.concat([combined_kosdaq_df, filtered_last_row_selected_columnsQ], ignore_index=True)

# 결과 출력
print("KOSPI 각 티커별 마지막 행 데이터:")
print(combined_kospi_df.tail())
print("\nKOSDAQ 각 티커별 마지막 행 데이터:")
print(combined_kosdaq_df.tail())

# 상승률 지표별로 조건을 만족하는 주식들을 분류하여 저장할 딕셔너리 초기화
rate_criteria = ['Daily_Gain_Rate', 'Weekly_Gain_Rate', 'Monthly_Gain_Rate', '30days_Gain_Rate', '90days_Gain_Rate']
kospi_stocks_by_rate = {rate: [] for rate in rate_criteria}
kosdaq_stocks_by_rate = {rate: [] for rate in rate_criteria}

def filter_stocks_higher_than_last_row(df, rate_criteria):
    stocks_by_rate = {rate: [] for rate in rate_criteria}
    # 마지막 행 가져오기
    last_row = df.iloc[-1]
    # 각 상승률 지표별로 처리
    for rate in rate_criteria:
        last_value = last_row[rate]
        for _, row in df.iterrows():
            if row[rate] > last_value:
                stocks_by_rate[rate].append((row['Name'], row['Ticker']))
    return stocks_by_rate

# KOSPI 및 KOSDAQ 데이터프레임 처리
kospi_stocks_by_rate = filter_stocks_higher_than_last_row(combined_kospi_df, rate_criteria)
kosdaq_stocks_by_rate = filter_stocks_higher_than_last_row(combined_kosdaq_df, rate_criteria)

# 결과 출력
def print_filtered_stocks(stocks_by_rate, market_name):
    print(f"{market_name} 시장의 각 상승률 지표별 조건을 만족하는 주식들:")
    for rate in rate_criteria:
        print(f"\n{rate} 보다 큰 주식들:")
        for name, ticker in stocks_by_rate[rate]:
            print(f"{name} : {ticker}")

print_filtered_stocks(kospi_stocks_by_rate, "KOSPI")
print_filtered_stocks(kosdaq_stocks_by_rate, "KOSDAQ")
