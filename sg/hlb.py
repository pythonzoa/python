import pandas as pd
import FinanceDataReader as fdr

# 설정
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# 기간 설정
start_date = '20200901'
end_date = '20241231'

# KRX 전체 종목 코드 불러오기
krx_list = fdr.StockListing('KRX')
stock_cap = krx_list[krx_list['Marcap'] >= 1e12][['Code', 'Name']]
random_stock_codes = stock_cap['Code'].tolist()
stock_cap = krx_list[['Code', 'Name', 'Marcap']]

# 각 종목에 대해 일별 데이터 불러오고 -29% 이상 하락한 날짜 추출
significant_drops = pd.DataFrame()

for code in stock_cap['Code']:
    # 종목별 일별 시세 데이터 불러오기
    df = fdr.DataReader(code, start_date, end_date)

    # 전일 종가 (preClose) 열 생성
    df['preClose'] = df['Close'].shift(1)

    # 전일 대비 하락률 계산 (%)
    df['Pct_change'] = (df['Close'] - df['preClose']) / df['preClose'] * 100

    df['MarketCap'] = df['Close'] * df['Volume']


    # -29% 이상 하락하고 시가총액이 1조 이상인 날짜 필터링
    filtered_df = df[(df['Pct_change'] <= -15) & (df['MarketCap'] >= 1e10)].copy()
    print(filtered_df)

    # 5, 20, 60 거래일 후의 종가 및 퍼센트 변동 계산
    shift_days = [5, 20, 60]
    for shift_day in shift_days:
        df[f'Close_{shift_day}d'] = df['Close'].shift(-shift_day)
        df[f'Pct_change_{shift_day}d'] = ((df[f'Close_{shift_day}d'] - df['Close']) / df['Close']) * 100

    # 결과가 존재할 경우 종합 데이터프레임에 추가
    if not filtered_df.empty:
        for shift_day in shift_days:
            filtered_df[f'Close_{shift_day}d'] = df.loc[filtered_df.index, f'Close_{shift_day}d']
            filtered_df[f'Pct_change_{shift_day}d'] = df.loc[filtered_df.index, f'Pct_change_{shift_day}d']

        filtered_df['Code'] = code
        filtered_df['Name'] = stock_cap.loc[stock_cap['Code'] == code, 'Name'].iloc[0]
        significant_drops = pd.concat([significant_drops, filtered_df], axis=0)

# 결과 출력
print(significant_drops[['Code', 'Name', 'Close', 'preClose', 'Pct_change', 'MarketCap', 'Close_5d', 'Pct_change_5d', 'Close_20d',
                         'Pct_change_20d', 'Close_60d', 'Pct_change_60d']])

# 결과를 엑셀 파일로 저장
significant_drops.to_excel('hahanga.xlsx')
