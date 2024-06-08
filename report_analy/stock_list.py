########## 현존하는 회사 LIST 찾기 완료 ###################
import io
import zipfile
import requests
from xml.etree.ElementTree import parse
import pandas as pd
import time
from workalendar.asia import SouthKorea
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import json

crtfc_key='825afc8affaa9a62a0a8e3425a6ce9cd71ab9c95'

#회사정보 가져오기
#임의로 'D:/' 로 설정 및 다운로드 파일 corpcode.zip으로 설정
path='D:/'
filename='corpcode.zip'

url = 'https://opendart.fss.or.kr/api/corpCode.xml'
params = {
    'crtfc_key': crtfc_key,
}
results=requests.get(url, params=params)

file = open(path+filename, 'wb')
file.write(results.content)
file.close()

zipfile.ZipFile(path+filename).extractall(path)

tree = parse(path + 'CORPCODE.xml')
root = tree.getroot()
li=root.findall('list')
corp_code,corp_name,stock_code,modify_date=[],[],[],[]
for d in li:
    corp_code.append(d.find('corp_code').text)
    corp_name.append(d.find('corp_name').text)
    stock_code.append(d.find('stock_code').text)
    modify_date.append(d.find('modify_date').text)
corps_df = pd.DataFrame({'corp_code':corp_code,'corp_name':corp_name,
         'stock_code':stock_code,'modify_date':modify_date})

corps_df = corps_df.loc[corps_df['stock_code']!=' ',:].reset_index(drop=True)
print(corps_df)

# 엑셀 파일로 저장
excel_file_path = path + '회사리스트.xlsx'  # 저장할 엑셀 파일 경로 및 이름 설정
corps_df.to_excel(excel_file_path, index=False, engine='openpyxl')  # 인덱스를 제외하고 저장

print(f"{excel_file_path}에 저장되었습니다.")
