########### 공시 보고서명에 따른 종목코드와 보고서 날짜 ###########
import requests
import pandas as pd
from datetime import datetime, timedelta

# OpenDART API 인증키 설정
crtfc_key = '825afc8affaa9a62a0a8e3425a6ce9cd71ab9c95'

# 0.2년씩 나누어 5번 실행
for i in range(4,10):
    # 조회할 기간 설정 (현재부터 0.2년 * (i+1) 전까지, 0.2년 단위로 데이터 조회)
    to_years = 0.5 * i
    from_years = 0.5 * (i + 1)
    end_date = datetime.now() - timedelta(days=365 * to_years)
    start_date = datetime.now() - timedelta(days=365 * from_years)

    # 결과를 저장할 DataFrame 초기화
    results_all = pd.DataFrame()

    # 10일 단위로 데이터 조회
    current_start_date = start_date
    while current_start_date < end_date:
        # 시작일로부터 10일 후를 종료일로 설정
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
            # 'list' 키의 존재 여부를 확인하여 결과가 있는지 검사
            if 'list' in results:
                results_df = pd.DataFrame(results['list'])
                results_all = pd.concat([results_all, results_df], ignore_index=True)

                total_page = results['total_page']
                if page_no >= total_page:
                    break
                page_no += 1

            else:
                print(2)
                break  # 결과가 없으면 반복 종료

        # 시작일 업데이트
        current_start_date = current_end_date + timedelta(days=1)

    ###################### 필터링할 키워드 설정 ###########################
    key = '무상증자'
    keyword_m = f'{key}|무상증자' # 포함될 키워드
    keyword_u = '가나다'  # 제외될 키워드

    # 필터링된 공시 정보 추출
    results_mj = results_all[
        results_all['report_nm'].str.contains(keyword_m) & ~results_all['report_nm'].str.contains(keyword_u)]
    results_mj = results_mj.drop_duplicates()

    print(results_mj)

    report_code = results_mj[['corp_name','corp_code','rcept_dt','stock_code']]

    print(report_code)

    ###################### 파일명 설정 ###########################
    excel_file_path = f'{key}_{i+1}.xlsx'  # 저장할 엑셀 파일 경로 및 이름 설정
    report_code.to_excel(excel_file_path, index=False, engine='openpyxl')  # 인덱스를 제외하고 저장

    print(f"{excel_file_path}에 저장되었습니다.")

