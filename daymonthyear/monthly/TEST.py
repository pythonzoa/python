import FinanceDataReader as fdr
import pandas as pd

# Pandas 출력 옵션 조정
pd.set_option('display.max_columns', None)  # 모든 컬럼 출력

# 종목 코드와 종목명 매핑
symbols = {
    'KS11': '코스피',
    'KQ11': '코스닥'
}

# 결과를 저장할 딕셔너리 초기화
dataframes = {}

for symbol, name in symbols.items():
    # 일별 데이터 추출
    daily_data = fdr.DataReader(symbol, '1999-12-26')

    # 일별 데이터를 월봉 데이터로 변환
    monthly_open = daily_data['Open'].resample('ME').first()
    monthly_close = daily_data['Close'].resample('ME').last()

    # '시가'와 '종가'를 포함하는 월봉 데이터 DataFrame 생성
    monthly_data = pd.DataFrame({'시가': monthly_open, '종가': monthly_close})
    monthly_data['월'] = monthly_data.index.month
    monthly_data['양봉여부'] = monthly_data['종가'] > monthly_data['시가']
    monthly_data['전월대비 상승 여부'] = monthly_data['종가'].diff() > 0
    monthly_data['상승률(%)'] = (monthly_data['종가'].diff() / monthly_data['종가'].shift(1)) * 100

    # 결과 저장
    dataframes[name] = monthly_data

# 각 DataFrame에 대한 월별 누적 수익률과 평균 수익률 계산
for name, df in dataframes.items():
    df['양봉개수'] = df.groupby('월')['양봉여부'].transform('sum')
    df['상승개수'] = df.groupby('월')['전월대비 상승 여부'].transform('sum')
    df['월별 누적 수익률'] = df.groupby('월')['상승률(%)'].transform('sum')
    df['월별 평균 수익률'] = df.groupby('월')['상승률(%)'].transform('mean')
    # 첫 번째 행(첫 월의 데이터) 제거
    df = df[1:]
    # 결과 저장
    dataframes[name] = df

# 결과 출력
for name, df in dataframes.items():
    print(f"{name} 데이터:")
    print(df.head(), '\n')
    df.to_excel(f"{name} month.xlsx")
