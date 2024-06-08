############ 시트 분리안하고 이어 붙이는 파일 ###########
import os
import pandas as pd
from bs4 import BeautifulSoup
import io  # StringIO를 사용하기 위해 필요

# 폴더 경로 설정
folder_path = r'D:\\'

# 폴더 내의 모든 HTML 파일 목록을 가져옴
html_files = [file for file in os.listdir(folder_path) if file.endswith('.html')]

# 최종 데이터를 저장할 빈 데이터프레임 생성
final_df = pd.DataFrame()

# 각 HTML 파일에 대해 처리
for html_file in html_files:
    # HTML 파일의 전체 경로
    file_path = os.path.join(folder_path, html_file)

    # HTML 파일 열기
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(html_content, 'html.parser')

    # <table> 태그 찾기
    tables = soup.find_all('table')

    for table in tables:
        # HTML 테이블 문자열을 StringIO 객체로 변환
        table_html_io = io.StringIO(str(table))

        # StringIO 객체를 사용하여 pandas로 HTML 데이터 읽기
        df = pd.read_html(table_html_io)[0]

        # 원본 HTML 파일명을 첫 번째 열로 추가
        df.insert(0, '파일명', html_file)

        # 최종 데이터프레임에 현재 데이터프레임 추가
        final_df = pd.concat([final_df, df], ignore_index=True)

    print(f"{html_file}에서 데이터 추출 및 추가 완료!")

# 최종 데이터를 Excel 파일에 저장
final_df.to_excel(os.path.join(folder_path, '통합_데이터.xlsx'), index=False)

print("모든 파일 처리 및 통합 저장 완료!")
