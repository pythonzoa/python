import OpenDartReader
import pandas as pd
import requests
from xml.etree.ElementTree import parse
from io import BytesIO, StringIO
from zipfile import ZipFile

# def download_krx_stock_codes():
#     url = "http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13"
#     response = requests.get(url)
#     response.encoding = 'cp949'  # 응답 인코딩을 'cp949'로 설정
#     html_content = StringIO(response.text)
#     df = pd.read_html(html_content, header=0)[0]
#     df['종목코드'] = df['종목코드'].map('{:06d}'.format)
#     return df[['회사명', '종목코드']].set_index('회사명')['종목코드'].to_dict()
#
# # 사용 예
# corp_dict = download_krx_stock_codes()
# print(corp_dict)
corp_dict = {'링네트': '042500'}


api_key = '825afc8affaa9a62a0a8e3425a6ce9cd71ab9c95'
dart = OpenDartReader(api_key)
corp_dict = {'링네트': '042500'}

def fetch_free_increase_events(corp_dict):
    results = []
    for name, code in corp_dict.items():  # key와 value 명확하게 분리
        try:
            event_data = dart.event(code, '무상증자')
            print(event_data)
            event_data.to_csv("free_increase_events.csv", index=False, encoding='cp949')
            if event_data:
                print('hi')
                event_data['corp_name'] = name  # 회사명 추가
                results.append(event_data)
            else:
                print(f"No data found for corp code {code} ({name})")
        except Exception as e:
            print(f"Error fetching data for corp code {code} ({name}): {e}")
    return results

# 회사 코드와 이름이 포함된 딕셔너리에서 무상증자 이벤트 데이터 수집
free_increase_events = fetch_free_increase_events(corp_dict)

if free_increase_events:  # 결과 데이터가 있는 경우에만 DataFrame 생성
    df = pd.DataFrame(free_increase_events)
    df.to_csv("free_increase_events.csv", index=False)
else:
    print("No events to save to CSV.")