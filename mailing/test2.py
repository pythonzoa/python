import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
from mailing import gmail

def fetch_news_by_titles(keywords, max_results_per_keyword=5):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

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
        if results_found == 0:
            print("해당 키워드로는 결과를 찾을 수 없습니다.")
        print()

fetch_news_by_titles(gmail.first_elements, 5)
