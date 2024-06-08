import OpenDartReader
import pandas as pd
import requests
from io import StringIO

# KRX로부터 주식 코드를 다운로드하고 딕셔너리로 반환하는 함수
def download_krx_stock_codes():
    url = "http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13"
    response = requests.get(url)
    response.encoding = 'cp949'
    html_content = StringIO(response.text)
    df = pd.read_html(html_content, header=0)[0]
    df['종목코드'] = df['종목코드'].map('{:06d}'.format)
    return df[['회사명', '종목코드']].set_index('회사명')['종목코드'].to_dict()

# 무상증자 이벤트 정보를 수집하는 함수
def fetch_free_increase_events(corp_dict, api_key):
    dart = OpenDartReader(api_key)
    results = []
    for name, code in corp_dict.items():
        try:
            print(code)
            event_data = dart.event(code, '무상증자')
            print(event_data)
            if not event_data.empty:
                event_data['회사명'] = name
                results.append(event_data)
            else:
                print(f"{name}({code})에 대한 무상증자 데이터가 없습니다.")
        except Exception as e:
            print(f"{name}({code}) 데이터 조회 중 오류 발생: {e}")
    # 모든 결과를 하나의 DataFrame으로 병합
    if results:
        return pd.concat(results)
    else:
        return pd.DataFrame()

# 메인 실행 부분
corp_dict = download_krx_stock_codes()
api_key = '825afc8affaa9a62a0a8e3425a6ce9cd71ab9c95'
free_increase_events = fetch_free_increase_events(corp_dict, api_key)

# 결과 데이터 저장
if not free_increase_events.empty:
    free_increase_events.to_csv("free_increase_events.csv", index=False, encoding='cp949')
    print("데이터를 CSV 파일로 저장하였습니다.")
else:
    print("저장할 무상증자 이벤트가 없습니다.")
