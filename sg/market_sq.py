from pykrx import stock
import pandas as pd
import FinanceDataReader as fdr

df = stock.get_market_trading_value_by_date("20030101", "20241231", "KOSPI")

# '개인' 컬럼 값이 1조 이상인 경우만 필터링
df_filtered = df[(df['개인'] >= 1_000_000_000_000) & (df['외국인합계'] <= -1_000_000_000_000)]

# 코스피 지수 데이터 가져오기
kospi = fdr.DataReader('KS11', '1990-01-01', '2024-12-31')

# '종가' 컬럼 이름을 'Close'로 변경
kospi.rename(columns={'Close': '종가'}, inplace=True)

# 'df_filtered'의 인덱스가 날짜일 경우를 가정
df_filtered.index = pd.to_datetime(df_filtered.index)

# 5, 20, 60 거래일 뒤의 주가와 수익률 계산
df_filtered['5일 뒤 종가'] = kospi['종가'].shift(-5).reindex(df_filtered.index)
df_filtered['20일 뒤 종가'] = kospi['종가'].shift(-20).reindex(df_filtered.index)
df_filtered['60일 뒤 종가'] = kospi['종가'].shift(-60).reindex(df_filtered.index)

# 수익률 계산
df_filtered['5일 뒤 수익률'] = (df_filtered['5일 뒤 종가'] - kospi['종가'].reindex(df_filtered.index)) / kospi['종가'].reindex(df_filtered.index)
df_filtered['20일 뒤 수익률'] = (df_filtered['20일 뒤 종가'] - kospi['종가'].reindex(df_filtered.index)) / kospi['종가'].reindex(df_filtered.index)
df_filtered['60일 뒤 수익률'] = (df_filtered['60일 뒤 종가'] - kospi['종가'].reindex(df_filtered.index)) / kospi['종가'].reindex(df_filtered.index)

# 결과 출력
print(df_filtered)

df_filtered.to_excel('marketsg1.xlsx')
# 필터링된 데이터 출력
print(df_filtered)


