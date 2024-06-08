import pandas as pd

# 영문 컬럼명과 한글 컬럼명을 리스트로 정의
english_columns = [
    'rcept_no', 'corp_cls', 'corp_code', 'corp_name', 'nstk_ostk_cnt',
    'nstk_estk_cnt', 'fv_ps', 'bfic_tisstk_ostk', 'bfic_tisstk_estk',
    'nstk_asstd', 'nstk_ascnt_ps_ostk', 'nstk_ascnt_ps_estk',
    'nstk_dividrk', 'nstk_dlprd', 'nstk_lstprd', 'bddd',
    'od_a_at_t', 'od_a_at_b', 'adt_a_atn'
]

korean_columns = [
    '접수번호', '법인구분', '고유번호', '회사명', '신주의 종류와 수(보통주식)',
    '신주의 종류와 수(기타주식)', '1주당 액면가액', '증자전 발행주식총수(보통주식)',
    '증자전 발행주식총수(기타주식)', '신주배정기준일', '1주당 신주배정 주식수(보통주식)',
    '1주당 신주배정 주식수(기타주식)', '신주의 배당기산일', '신주권교부예정일',
    '신주의 상장 예정일', '이사회결의일(결정일)', '사외이사 참석여부(참석)',
    '사외이사 참석여부(불참)', '감사(감사위원)참석 여부'
]

# 영문 컬럼명과 한글 컬럼명을 포함하는 데이터프레임 생성
df_columns = pd.DataFrame({
    'English Column': english_columns,
    'Korean Column': korean_columns
})

# 데이터프레임 출력
print(df_columns)

df_columns.to_excel('go.xlsx')