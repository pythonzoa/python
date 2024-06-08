import FinanceDataReader as fdr
import pandas as pd
import numpy as np
from scipy import stats

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)
pd.set_option('display.expand_frame_repr', False)

# 전체 기간 데이터 가져오기 (2014-01-01 ~ 2023-12-31)
start_date = "2014-01-01"
end_date = "2023-12-31"

# 조회할 지수 목록
indexes = ["KS11", "KQ11"]

# 결과를 저장할 데이터프레임
total_results = {}

for index in indexes:
    total_results[index] = fdr.DataReader(index, start_date, end_date)

# 날짜 목록
dates = [
    "2014-03-13", "2014-06-12", "2014-09-11", "2014-12-11",
    "2015-03-12", "2015-06-11", "2015-09-10", "2015-12-10",
    "2016-03-10", "2016-06-09", "2016-09-08", "2016-12-08",
    "2017-03-09", "2017-06-08", "2017-09-14", "2017-12-14",
    "2018-03-08", "2018-06-14", "2018-09-13", "2018-12-13",
    "2019-03-14", "2019-06-13", "2019-09-12", "2019-12-12",
    "2020-03-12", "2020-06-11", "2020-09-10", "2020-12-10",
    "2021-03-11", "2021-06-10", "2021-09-09", "2021-12-09",
    "2022-03-10", "2022-06-09", "2022-09-08", "2022-12-08",
    "2023-03-09", "2023-06-08", "2023-09-14", "2023-12-14"
]

# 특정 날짜들의 데이터를 저장할 데이터프레임
specific_dates_results = pd.DataFrame(
    columns=["Date", "Index", "Open", "Close", "High", "Low", "Prev_Open", "Prev_Close", "Prev_High", "Prev_Low",
             "Open_Change", "Close_Change", "High_Change", "Low_Change"])

# 전체 기간 동안의 일일 상승률 계산
for index in indexes:
    total_results[index]['Prev_Open'] = total_results[index]['Open'].shift(1)
    total_results[index]['Prev_Close'] = total_results[index]['Close'].shift(1)
    total_results[index]['Prev_High'] = total_results[index]['High'].shift(1)
    total_results[index]['Prev_Low'] = total_results[index]['Low'].shift(1)
    total_results[index]['Open_Change'] = (total_results[index]['Open'] - total_results[index]['Prev_Open']) / \
                                          total_results[index]['Prev_Open']
    total_results[index]['Close_Change'] = (total_results[index]['Close'] - total_results[index]['Prev_Close']) / \
                                           total_results[index]['Prev_Close']
    total_results[index]['High_Change'] = (total_results[index]['High'] - total_results[index]['Prev_High']) / \
                                          total_results[index]['Prev_High']
    total_results[index]['Low_Change'] = (total_results[index]['Low'] - total_results[index]['Prev_Low']) / \
                                         total_results[index]['Prev_Low']

# 특정 날짜에 대한 데이터 추출
for date in dates:
    for index in indexes:
        if date in total_results[index].index:
            data = total_results[index].loc[date]
            prev_data = total_results[index].shift(1).loc[date]
            if not data.isna().any() and not prev_data.isna().any():
                new_row = pd.DataFrame({
                    "Date": [date],
                    "Index": [index],
                    "Open": [data["Open"]],
                    "Close": [data["Close"]],
                    "High": [data["High"]],
                    "Low": [data["Low"]],
                    "Prev_Open": [prev_data["Open"]],
                    "Prev_Close": [prev_data["Close"]],
                    "Prev_High": [prev_data["High"]],
                    "Prev_Low": [prev_data["Low"]],
                    "Open_Change": [(data["Open"] - prev_data["Open"]) / prev_data["Open"]],
                    "Close_Change": [(data["Close"] - prev_data["Close"]) / prev_data["Close"]],
                    "High_Change": [(data["High"] - prev_data["High"]) / prev_data["High"]],
                    "Low_Change": [(data["Low"] - prev_data["Low"]) / prev_data["Low"]]
                })
                # new_row가 비어 있지 않은지 확인하고 결합
                if not new_row.dropna().empty:
                    specific_dates_results = pd.concat([specific_dates_results, new_row], ignore_index=True)

# 전체 기간 동안의 상승률의 평균과 표준 편차 계산
change_stats = {index: {
    'Open_mean': total_results[index]['Open_Change'].mean(), 'Open_std': total_results[index]['Open_Change'].std(),
    'Close_mean': total_results[index]['Close_Change'].mean(), 'Close_std': total_results[index]['Close_Change'].std(),
    'High_mean': total_results[index]['High_Change'].mean(), 'High_std': total_results[index]['High_Change'].std(),
    'Low_mean': total_results[index]['Low_Change'].mean(), 'Low_std': total_results[index]['Low_Change'].std()
} for index in indexes}

# 각 만기일의 Open, Close, High, Low 값이 평균 대비 유의미하게 다른지 검증
t_test_results = []

for date in dates:
    for index in indexes:
        if date in total_results[index].index:
            overall_data = total_results[index]
            expiry_data = specific_dates_results[
                (specific_dates_results['Date'] == date) & (specific_dates_results['Index'] == index)]

            if not expiry_data.empty:
                for col in ['Open_Change', 'Close_Change', 'High_Change', 'Low_Change']:
                    t_stat, p_value = stats.ttest_1samp(overall_data[col].dropna(), expiry_data[col].values[0])
                    t_test_results.append({
                        "Date": date,
                        "Index": index,
                        "Measure": col,
                        "t_stat": t_stat,
                        "p_value": p_value,
                        "mean_overall": overall_data[col].mean(),
                        "std_overall": overall_data[col].std(),
                        "expiry_value": expiry_data[col].values[0]
                    })

t_test_results_df = pd.DataFrame(t_test_results)

# 결과 출력
print("t-검정 결과:")
print(t_test_results_df)

if (t_test_results_df['p_value'] < 0.05).any():
    print("만기일의 변동성이 통계적으로 유의미하게 큽니다.")
else:
    print("만기일의 변동성이 평균 변동성과 통계적으로 유의미하게 다르지 않습니다.")

# 엑셀 파일로 저장
specific_dates_results.to_excel('specific_dates_results.xlsx')
t_test_results_df.to_excel('t_test_results.xlsx')
