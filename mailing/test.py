import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 경로 설정
# Windows 예시: 'C:\\Windows\\Fonts\\malgun.ttf'
# MacOS 예시: '/System/Library/Fonts/Supplemental/AppleGothic.ttf'
# Linux 예시: '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
font_path = r'C:\Users\TMS\AppData\Local\Microsoft\Windows\Fonts\NanumGothic.ttf'

# 폰트 프로퍼티 설정 및 matplotlib의 기본 폰트 변경
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)
plt.rcParams['axes.unicode_minus'] = False  # 음수 부호 오류 방지

# 예제 데이터 리스트
data = [('항목1', 10), ('항목2', 15), ('항목3', 7), ('항목4', 20)]

# 데이터 분리
labels, values = zip(*data)

# 바 차트 생성
plt.figure(figsize=(10, 6))  # 그래프 크기 설정
plt.bar(labels, values, color='skyblue')  # 바 차트 그리기
plt.xlabel('항목')  # x축 레이블
plt.ylabel('값')  # y축 레이블
plt.title('리스트 데이터 바 차트')  # 그래프 제목
plt.xticks(rotation=45)  # x축 레이블 회전
plt.tight_layout()  # 레이아웃 조정

# 그림 파일로 저장
plt.savefig('list_data_chart.jpg', dpi=300)  # 변경된 저장 경로
plt.close()
