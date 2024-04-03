import requests
from bs4 import BeautifulSoup

def fetch_specific_news_about(keyword, contained_in_title, max_results=10):
    # 검색 URL 설정
    url = f"https://www.google.com/search?q={keyword}&tbm=nws"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results_found = 0
    for a in soup.find_all('a', href=True):
        if results_found >= max_results:
            break
        title = a.text
        link = a['href']
        if contained_in_title in title:
            print(f"제목: {title}")
            print(f"링크: {link}")
            print('-' * 100)
            results_found += 1

# '동진쎄미켐' 관련 뉴스 중 제목에 '동진쎄미켐'이 포함된 뉴스 10개 추출
fetch_specific_news_about('동진쎄미켐', '동진쎄미켐', 10)
