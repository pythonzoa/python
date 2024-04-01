import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
import pandas as pd
import shutil
import os
import re
from daily_alram import sichong, vs_market
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

today = datetime.now().strftime('%Y-%m-%d')

def validate_and_clean_data(data):
    # 데이터 길이가 가장 긴 열을 기준으로 모든 열의 길이를 맞춥니다.
    max_len = max(len(lst) for lst in data.values())
    # 모든 열에 대해 길이를 확인하고, 짧은 열은 None으로 채워 길이를 맞춥니다.
    adjusted_data = {key: lst + [None] * (max_len - len(lst)) for key, lst in data.items()}
    return adjusted_data

def zip_folder(folder_path, output_path, archive_name):
    shutil.make_archive(f"{output_path}/{archive_name}", 'zip', folder_path)

def find_latest_folder(directory):
    # 날짜와 시간 형식의 폴더 이름 패턴 정의
    pattern = re.compile(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}')

    # 디렉토리 내의 모든 폴더를 찾되, 정의된 패턴과 일치하는 이름만 고려합니다.
    folders = [os.path.join(directory, f) for f in os.listdir(directory)
               if os.path.isdir(os.path.join(directory, f)) and pattern.match(f)]
    # 각 폴더의 생성 시간을 기준으로 가장 최근 폴더를 찾습니다.
    if folders:
        latest_folder = max(folders, key=os.path.getctime)
        return latest_folder
    else:
        return None

def find_duplicate_values():
    # sichong.kospi_stocks_by_rate 데이터 로드
    kospi_stocks = sichong.kospi_stocks_by_rate
    kosdaq_stocks = sichong.kosdaq_stocks_by_rate
    # 'Daily_Gain_Rate'와 '30days_Gain_Rate' 열의 값 추출
    daily_gain_rate_values = kospi_stocks['Daily_Gain_Rate']
    days30_gain_rate_values = kospi_stocks['30days_Gain_Rate']

    daily_gain_rate_valuesQ = kosdaq_stocks['Daily_Gain_Rate']
    days30_gain_rate_valuesQ = kosdaq_stocks['30days_Gain_Rate']

    # 중복되는 값 찾기
    duplicate_values = [value for value in daily_gain_rate_values if value in days30_gain_rate_values]
    duplicate_valuesQ = [value for value in daily_gain_rate_valuesQ if value in days30_gain_rate_valuesQ]

    # 두 리스트의 중복된 값들을 합치고 중복 제거
    combined_duplicates = list(set(duplicate_values + duplicate_valuesQ))

    # 중복 제거된 리스트 반환
    return combined_duplicates

# 함수 호출 및 중복된 값들 출력
duplicate_values_list = find_duplicate_values()
# 첫 번째 요소들만 추출하여 리스트 생성
first_elements = [t[0] for t in duplicate_values_list]

def fetch_news_by_titles(keywords, max_results_per_keyword=5):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    news_data = {'Keyword': [], 'Title': [], 'URL': []}  # 뉴스 데이터를 저장할 딕셔너리

    for keyword in keywords:
        print(f"검색 키워드: {keyword} 관련 뉴스")
        url = f"https://www.google.com/search?q={keyword}&tbm=nws"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        results_found = 0
        for a in soup.find_all('a', href=True):
            if results_found >= max_results_per_keyword:
                break
            if '/url?esrc=' in a['href']:
                parsed_url = urlparse(a['href'])
                query_params = parse_qs(parsed_url.query)
                real_url = query_params.get('url', [None])[0]
                title = a.text
                if real_url:
                    print(f"제목: {title}")
                    print(f"URL: {real_url}")
                    print('-' * 100)
                    results_found += 1

                    # 결과를 딕셔너리에 추가
                    news_data['Keyword'].append(keyword)
                    news_data['Title'].append(title)
                    news_data['URL'].append(real_url)

        if results_found == 0:
            print("해당 키워드로는 결과를 찾을 수 없습니다.")
        print()

    # DataFrame 생성
    df = pd.DataFrame(news_data)

    # 엑셀 파일로 저장
    df.to_excel(f'{today}_Strong_News.xlsx', index=False)

# 함수 호출
fetch_news_by_titles(first_elements, 5)

def do_something():
    # sichong 모듈에서 데이터를 가져와 DataFrame으로 변환합니다.
    kospi_df = pd.DataFrame(sichong.combined_kospi_df)
    kosdaq_df = pd.DataFrame(sichong.combined_kosdaq_df)

    # 비율 데이터를 정제하여 DataFrame으로 변환합니다.
    kospi_rate_data_cleaned = validate_and_clean_data(sichong.kospi_stocks_by_rate)
    kospi_rate_df = pd.DataFrame(kospi_rate_data_cleaned)

    kosdaq_rate_data_cleaned = validate_and_clean_data(sichong.kosdaq_stocks_by_rate)
    kosdaq_rate_df = pd.DataFrame(kosdaq_rate_data_cleaned)

    # 오늘 날짜를 문자열로 포맷합니다.
    today = datetime.now().strftime('%Y-%m-%d')

    # Excel 파일로 데이터를 저장합니다.
    excel_filename = f"{today} 시장보다 강한 종목.xlsx"
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        kospi_df.to_excel(writer, sheet_name='시총 큰 KOSPI', index=False)
        kosdaq_df.to_excel(writer, sheet_name='시총 큰 KOSDAQ', index=False)
        kospi_rate_df.to_excel(writer, sheet_name='시장보다 강한 종목 KOSPI', index=False)
        kosdaq_rate_df.to_excel(writer, sheet_name='시장보다 강한 종목 KOSDAQ', index=False)

    # 이메일 설정 및 생성
    sender_email = "onlyhalfgp@gmail.com"
    recipient_email = "onlyhalfgp@gmail.com"
    subject = f'[{today}] 시장보다 강한 종목'
    body = f"{today} 시장보다 강한 종목"

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Excel 파일을 이메일에 첨부합니다.
    with open(excel_filename, "rb") as file:
        part = MIMEApplication(file.read(), Name=os.path.basename(excel_filename))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(excel_filename)}"'
        message.attach(part)

    with open(f"{today}_Strong_News.xlsx", "rb") as file:
        part = MIMEApplication(file.read(), Name=f'{today}_Strong_News.xlsx')
        part['Content-Disposition'] = f'attachment; filename="{today}_Strong_News.xlsx"'
        message.attach(part)

    # 가장 최근에 생성된 날짜 형식 폴더를 찾아 압축
    latest_folder_path = find_latest_folder(r"C:\Users\TMS\PycharmProjects\StrongStocks\mailing")  # 검색할 디렉토리 경로
    if latest_folder_path:
        zip_output_path = "."  # 압축 파일이 저장될 경로
        zip_archive_name = os.path.basename(latest_folder_path)  # 압축 파일의 이름을 최근 폴더 이름으로 설정
        zip_folder(latest_folder_path, zip_output_path, zip_archive_name)  # 폴더 압축
        zip_file_path = f"{zip_output_path}/{zip_archive_name}.zip"

        # 압축 파일을 이메일에 첨부
        with open(zip_file_path, "rb") as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(zip_file_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_file_path)}"'
            message.attach(part)
    else:
        print("날짜 형식에 맞는 최근 폴더를 찾을 수 없습니다.")

    # 이메일 전송
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "onlyhalfgp@gmail.com"
    smtp_password = "slks mqtq tppd jhtz"

    with smtplib.SMTP(smtp_server,  smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, message.as_string())
        server.quit()


if __name__ == "__main__":
    do_something()
