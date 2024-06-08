import FinanceDataReader as fdr
import pandas as pd
import datetime as dt

# 데이터를 가져올 기간 설정
start_date = '2023-10-01'
end_date = '2024-12-31'

# KOSPI 지수 데이터 가져오기
kospi_data = fdr.DataReader('KS11', start=start_date, end=end_date)

# 데이터의 인덱스를 datetime 형식으로 변환
kospi_data.index = pd.to_datetime(kospi_data.index)

# 주별로 리샘플링하고, 각 주의 월요일 데이터를 추출
weekly_data = kospi_data.resample('W-MON').first()

# 각 주의 첫 거래일을 찾기 위해 이터레이션
first_trading_days = []
for i in range(1, len(weekly_data)):
    current_monday = weekly_data.index[i]
    last_friday = current_monday - dt.timedelta(days=3)

    if last_friday not in kospi_data.index:
        # 전주 금요일이 휴장일 경우, 다음 거래일을 찾습니다.
        last_friday_value = None
    else:
        last_friday_value = kospi_data.loc[last_friday, 'Close']

    current_monday_value = weekly_data.loc[current_monday, 'Close']

    # 월요일과 전주 금요일의 종가 비교
    if last_friday_value == current_monday_value:
        # 종가가 같다면 공휴일로 간주하고, 다음 거래일을 찾습니다.
        next_day = current_monday + dt.timedelta(days=1)
        while next_day not in kospi_data.index:
            next_day += dt.timedelta(days=1)
        first_trading_days.append(next_day)
    else:
        # 종가가 다르다면 그날이 첫 거래일입니다.
        first_trading_days.append(current_monday)

# 결과 출력
print(first_trading_days)
