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
