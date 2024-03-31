import FinanceDataReader as fdr

# KRX 상장 회사 목록을 불러옴
krx_list = fdr.StockListing('KRX')

# 시가총액이 1조 원 이상인 KOSPI 상장 회사 추출
kospi_over_1t = krx_list[(krx_list['Market'] == 'KOSPI') & (krx_list['Marcap'] >= 1e13)][['Code', 'Name', 'Market', 'Marcap']]

# 시가총액이 1조 원 이상인 KOSDAQ 상장 회사 추출
kosdaq_over_1t = krx_list[(krx_list['Market'] == 'KOSDAQ') & (krx_list['Marcap'] >= 1e13)][['Code', 'Name', 'Market', 'Marcap']]

# 추출된 KOSPI 상장 회사들의 코드만 리스트로 변환
kospi_codes_over_1t = kospi_over_1t['Code'].tolist()

# 추출된 KOSDAQ 상장 회사들의 코드만 리스트로 변환
kosdaq_codes_over_1t = kosdaq_over_1t['Code'].tolist()


print("시가총액 1조 원 이상인 KOSPI 상장 회사:")
print(kospi_over_1t)

print("\n시가총액 1조 원 이상인 KOSDAQ 상장 회사:")
print(kosdaq_over_1t)

print("시가총액 1조 원 이상인 KOSPI 상장 회사 코드:")
print(kospi_codes_over_1t)

print("\n시가총액 1조 원 이상인 KOSDAQ 상장 회사 코드:")
print(kosdaq_codes_over_1t)