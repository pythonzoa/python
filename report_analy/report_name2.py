import requests
import pandas as pd
from datetime import datetime, timedelta

# OpenDART API 인증키 설정
crtfc_key = '825afc8affaa9a62a0a8e3425a6ce9cd71ab9c95'

# 결과를 저장할 DataFrame 초기화
results_all = pd.DataFrame()

# 0.5년 단위로 데이터 조회
for i in range(4):
    to_years = 0.5 * i
    from_years = 0.5 * (i + 1)
    end_date = datetime.now() - timedelta(days=365 * to_years)
    start_date = datetime.now() - timedelta(days=365 * from_years)

    # 10일 단위로 데이터 조회
    current_start_date = start_date
    while current_start_date < end_date:
        current_end_date = min(current_start_date + timedelta(days=10), end_date)
        bgn_de = current_start_date.strftime("%Y%m%d")
        end_de = current_end_date.strftime("%Y%m%d")

        # 페이지 번호 초기화
        page_no = 1
        page_count = 100

        # OpenDART API를 통해 공시 정보를 페이지별로 가져오기
        while True:
            url = 'https://opendart.fss.or.kr/api/list.json'
            params = {
                'crtfc_key': crtfc_key,
                'page_no': str(page_no),
                'page_count': str(page_count),
                'bgn_de': bgn_de,
                'end_de': end_de,
            }
            results = requests.get(url, params=params).json()

            if 'list' in results:
                results_df = pd.DataFrame(results['list'])
                results_all = pd.concat([results_all, results_df], ignore_index=True)
                if page_no >= results['total_page']:
                    break
                page_no += 1
            else:
                break
        current_start_date = current_end_date + timedelta(days=1)

# 중복 데이터 제거
results_all.drop_duplicates(inplace=True)

# 필터링할 키워드 설정
keyword_m = '무상증자'
results_all = results_all[results_all['report_nm'].str.contains(keyword_m, na=False)]

# 결과 저장
excel_file_path = f'{keyword_m}_공시_정보.xlsx'
results_all.to_excel(excel_file_path, index=False, engine='openpyxl')
print(f"{excel_file_path}에 저장되었습니다.")
