import pandas as pd
import FinanceDataReader as fdr


# 날짜 열의 이름을 확인한 후, 올바른 열 이름을 사용하여 데이터프레임을 다시 로드합니다.
# 예를 들어, 날짜 열의 이름이 'date'인 경우:
df = pd.read_excel(r'C:\Users\201-13\PycharmProjects\pythonProject\daily_alram\2024-05-27_20-30-22\days_21\KOSPI_KOSDAQ_Cumulative_Returns.xlsx', index_col='Date', parse_dates=True)

# 코스피 데이터 로드
kospi_data = fdr.DataReader('KS11', df.index.min(), df.index.max())

# 인덱스가 datetime 형식이라고 가정합니다.
kospi_data = kospi_data.sort_index()

# 5, 20, 60 거래일 뒤의 주가 컬럼을 생성하여 이동된 데이터프레임 생성
kospi_5d = kospi_data[['Close']].shift(-5).reset_index()
kospi_20d = kospi_data[['Close']].shift(-20).reset_index()
kospi_60d = kospi_data[['Close']].shift(-60).reset_index()

kospi_5d.columns = ['Date', 'KOSPI_5일후']
kospi_20d.columns = ['Date', 'KOSPI_20일후']
kospi_60d.columns = ['Date', 'KOSPI_60일후']

# 원본 데이터프레임의 인덱스를 reset_index하여 날짜를 컬럼으로 변환
df_reset = df.reset_index()

# 가장 가까운 날짜 매칭하여 새로운 컬럼 추가
df_merged = pd.merge_asof(df_reset, kospi_5d, on='Date')
df_merged = pd.merge_asof(df_merged, kospi_20d, on='Date')
df_merged = pd.merge_asof(df_merged, kospi_60d, on='Date')

# 인덱스를 다시 설정
df_final = df_merged.set_index('Date')

# 결과 확인
print(df_final.head())

# 데이터프레임을 저장하고 싶다면 다음과 같이 할 수 있습니다.
# df_final.to_excel('KOSPI_with_future_prices.xlsx')
