import FinanceDataReader as fdr
import pandas as pd
from scipy.stats import binomtest
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

# Pandas 출력 옵션 조정
pd.set_option('display.max_columns', None)  # 모든 컬럼 출력

def analyze_index_by_month(symbol, start_date, end_date, writer):
    data = fdr.DataReader(symbol, start=start_date, end=end_date)
    power_analysis = NormalIndPower()
    alpha = 0.05

    index_names = {
        'KS11': '코스피',
        'KQ11': '코스닥'
    }
    index_name = index_names.get(symbol, symbol)
    data.index = pd.to_datetime(data.index)

    all_results = []  # 모든 결과를 저장할 리스트

    for month in range(1, 13):
        monthly_data = data[data.index.month == month]

        if monthly_data.empty:
            continue

        monthly_agg = monthly_data.resample('ME').agg(
            {'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
        monthly_agg.dropna(inplace=True)
        monthly_agg.sort_index(inplace=True)

        monthly_agg['Prev Close'] = monthly_agg['Close'].shift(1)
        monthly_agg['Gap'] = monthly_agg['Open'] - monthly_agg['Prev Close']
        monthly_agg['Body'] = monthly_agg['Close'] - monthly_agg['Open']

        stats = {
            'Month': month,
            '종가 상승': (monthly_agg['Close'] > monthly_agg['Prev Close']).sum(),
            '종가 하락': (monthly_agg['Close'] < monthly_agg['Prev Close']).sum(),
            '갭 상승': (monthly_agg['Gap'] > 0).sum(),
            '갭 하락': (monthly_agg['Gap'] < 0).sum(),
            '양봉': (monthly_agg['Body'] > 0).sum(),
            '음봉': (monthly_agg['Body'] < 0).sum()
        }
        print(monthly_agg)

        for key, count in stats.items():
            if key == 'Month':
                continue
            observed_rate = count / len(monthly_agg) if len(monthly_agg) > 0 else 0
            p_value = binomtest(k=count, n=len(monthly_agg), p=0.5, alternative='greater').pvalue if len(
                monthly_agg) > 0 else 1

            all_results.append({
                'Month': f'{month}월',
                'Statistic': key,
                'Count': count,
                'P-Value': p_value
            })

    # 결과 데이터를 DataFrame으로 변환
    results_df = pd.DataFrame(all_results)
    # 엑셀 파일에 쓰기
    results_df.to_excel(writer, sheet_name=index_name)


def execute_monthly_analysis():
    index_symbols = ['KS11', 'KQ11']
    start_date = '1999-12-26'
    end_date = '2023-12-31'

    with pd.ExcelWriter('monthly_analysis_results_with_p_value_by_month.xlsx', engine='openpyxl') as writer:
        for symbol in index_symbols:
            analyze_index_by_month(symbol, start_date, end_date, writer)


execute_monthly_analysis()
