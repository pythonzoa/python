

import FinanceDataReader as fdr
import pandas as pd
from scipy.stats import binomtest
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

def analyze_index_combined(symbol, start_date, end_date):
    data = fdr.DataReader(symbol, start=start_date, end=end_date)
    periods = {
        '일봉': data,
        '주봉': data.resample('W-FRI').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'}),
        '월봉': data.resample('ME').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume': 'sum'})
    }

    power_analysis = NormalIndPower()
    alpha = 0.05  # 유의 수준

    # 심볼에 따른 지수 이름 매핑
    index_names = {
        'KS11': '코스피',
        'KQ11': '코스닥'
    }
    index_name = index_names.get(symbol, symbol)  # 심볼에 해당하는 이름을 가져오기

    for period_name, period_data in periods.items():
        print(f"{index_name} {period_name} 분석:")
        period_data['Prev Close'] = period_data['Close'].shift(1)
        period_data['Gap'] = period_data['Open'] - period_data['Prev Close']
        period_data['Body'] = period_data['Close'] - period_data['Open']

        stats = {
            '종가 상승': (period_data['Close'] > period_data['Prev Close']).sum(),
            '종가 하락': (period_data['Close'] < period_data['Prev Close']).sum(),
            '갭 상승': (period_data['Gap'] > 0).sum(),
            '갭 하락': (period_data['Gap'] < 0).sum(),
            '양봉': (period_data['Body'] > 0).sum(),
            '음봉': (period_data['Body'] < 0).sum()
        }
        total_days = len(period_data)

        for stat_name, count in stats.items():
            observed_rate = count / total_days
            effect_size = proportion_effectsize(observed_rate, 0.5)
            power = power_analysis.solve_power(effect_size=effect_size, nobs1=total_days, alpha=alpha,
                                               alternative='two-sided')

            p_value_greater = binomtest(k=count, n=total_days, p=0.5, alternative='greater').pvalue
            p_value_less = binomtest(k=count, n=total_days, p=0.5, alternative='less').pvalue

            print(f"{stat_name}: {count}/{total_days}, greater p-value: {p_value_greater:.4f}, less p-value: {p_value_less:.4f}, 검정의 힘: {power:.4f}")
            if p_value_greater < 0.05 or p_value_less < 0.05:
                print(f"  - {stat_name}의 비율이 통계적으로 유의미합니다.")
            if power >= 0.8:
                print(f"  - {stat_name}의 차이는 통계적으로 유의미하며, 검정의 힘이 충분합니다.")
            else:
                print(f"  - {stat_name}의 차이가 있을 수 있지만, 검정의 힘이 충분하지 않을 수 있습니다. 샘플 크기를 늘려 고려해 보세요.")
        print()

def execute_combined_analysis():
    index_symbols = ['KS11', 'KQ11']  # 분석할 지수 목록
    start_date = '2004-01-01'

    end_date = '2023-12-31'

    for symbol in index_symbols:
        analyze_index_combined(symbol, start_date, end_date)

# KOSPI와 KOSDAQ 지수에 대한 통합 분석 실행
execute_combined_analysis()