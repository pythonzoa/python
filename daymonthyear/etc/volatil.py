import FinanceDataReader as fdr
import pandas as pd
import numpy as np

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
specific_dates_results = pd.DataFrame(columns=["Date", "Index", "Open", "Close", "High", "Low", "Prev_Open", "Prev_Close", "Prev_High", "Prev_Low", "Open_Change", "Close_Change", "High_Change", "Low_Change"])

# 전체 기간 동안의 일일 상승률 계산
for index in indexes:
    total_results[index]['Prev_Open'] = total_results[index]['Open'].shift(1)
    total_results[index]['Prev_Close'] = total_results[index]['Close'].shift(1)
    total_results[index]['Prev_High'] = total_results[index]['High'].shift(1)
    total_results[index]['Prev_Low'] = total_results[index]['Low'].shift(1)
    total_results[index]['Open_Change'] = (total_results[index]['Open'] - total_results[index]['Prev_Open']) / total_results[index]['Prev_Open']
    total_results[index]['Close_Change'] = (total_results[index]['Close'] - total_results[index]['Prev_Close']) / total_results[index]['Prev_Close']
    total_results[index]['High_Change'] = (total_results[index]['High'] - total_results[index]['Prev_High']) / total_results[index]['Prev_High']
    total_results[index]['Low_Change'] = (total_results[index]['Low'] - total_results[index]['Prev_Low']) / total_results[index]['Prev_Low']

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

# 특정 날짜들의 상승률이 평균에서 얼마나 벗어나는지 확인
specific_dates_results['Open_Deviation'] = specific_dates_results.apply(lambda row: (row['Open_Change'] - change_stats[row['Index']]['Open_mean']) / change_stats[row['Index']]['Open_std'], axis=1)
specific_dates_results['Close_Deviation'] = specific_dates_results.apply(lambda row: (row['Close_Change'] - change_stats[row['Index']]['Close_mean']) / change_stats[row['Index']]['Close_std'], axis=1)
specific_dates_results['High_Deviation'] = specific_dates_results.apply(lambda row: (row['High_Change'] - change_stats[row['Index']]['High_mean']) / change_stats[row['Index']]['High_std'], axis=1)
specific_dates_results['Low_Deviation'] = specific_dates_results.apply(lambda row: (row['Low_Change'] - change_stats[row['Index']]['Low_mean']) / change_stats[row['Index']]['Low_std'], axis=1)

# z-점수를 기반으로 이례적인지 평균적인지 판단
def judge_deviation(deviation):
    if abs(deviation) <= 1.96:
        return '평균적 상황 (95% 신뢰구간 내)'
    elif abs(deviation) <= 2.576:
        return '다소 이례적 상황 (95% 신뢰구간 바깥, 99% 신뢰구간 내)'
    else:
        return '매우 이례적 상황 (99% 신뢰구간 바깥)'

specific_dates_results['Open_Judgement'] = specific_dates_results['Open_Deviation'].apply(judge_deviation)
specific_dates_results['Close_Judgement'] = specific_dates_results['Close_Deviation'].apply(judge_deviation)
specific_dates_results['High_Judgement'] = specific_dates_results['High_Deviation'].apply(judge_deviation)
specific_dates_results['Low_Judgement'] = specific_dates_results['Low_Deviation'].apply(judge_deviation)

# 결과 출력
print("전체 기간 동안의 상승률의 평균과 표준 편차:")
print(pd.DataFrame.from_dict(change_stats, orient='index'))

print("\n특정 날짜들의 상승률과 판단 결과:")
print(specific_dates_results)


specific_dates_results.to_excel('excel.xlsx')
