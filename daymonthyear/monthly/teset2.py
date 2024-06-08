import pandas as pd

# 예제 데이터프레임 생성 (인덱스가 datetime 타입이라고 가정)
rng = pd.date_range('2020-01-01', periods=12, freq='ME')  # 2020년 각 월의 마지막 날짜를 포함하는 날짜 범위 생성
df = pd.DataFrame({'값': range(12)}, index=rng)

# 인덱스에서 월 정보 추출하여 새로운 컬럼 '월'에 저장
df['월'] = df.index.month

# 결과 확인
print(df)
