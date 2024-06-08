import FinanceDataReader as fdr
import pandas as pd

# 엑셀 파일로 저장할 경로
excel_path = "monthly_data.xlsx"

def analyze_index_by_individual_month(symbol, start_date, end_date):
    # 데이터 불러오기
    data = fdr.DataReader(symbol, start=start_date, end=end_date)

    # 월별 데이터를 저장할 딕셔너리 초기화
    monthly_datas = {}

    # 각 월별 데이터 분석
    for month in range(1, 13):  # 1월부터 12월까지
        # 해당 월만 필터링하여 복사본 생성
        monthly_data = data[data.index.month == month].copy()

        if monthly_data.empty:
            print(f"{symbol} {month}월: 데이터가 없습니다.")
            continue

        # 직접 통계 계산 (여기에 필요한 계산 추가)
        monthly_data['Prev Close'] = monthly_data['Close'].shift(1)
        monthly_data['Gap'] = monthly_data['Open'] - monthly_data['Prev Close']
        monthly_data['Body'] = monthly_data['Close'] - monthly_data['Open']

        # 월별 데이터를 딕셔너리에 저장
        monthly_datas[month] = monthly_data

    return monthly_datas


def execute_monthly_analysis_and_save_to_excel():
    index_symbols = ['KS11', 'KQ11']
    start_date = '2000-01-01'
    end_date = '2023-12-31'

    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        for symbol in index_symbols:
            # 월별 데이터 분석 실행
            monthly_datas = analyze_index_by_individual_month(symbol, start_date, end_date)

            for month, df in monthly_datas.items():
                # 월별 데이터를 엑셀 파일의 별도 시트로 저장
                sheet_name = f"{symbol} {month}월"
                df.to_excel(writer, sheet_name=sheet_name)


execute_monthly_analysis_and_save_to_excel()
