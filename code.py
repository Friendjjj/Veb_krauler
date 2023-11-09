import requests
from bs4 import BeautifulSoup as BS

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
r = requests.get("https://stopgame.ru/review/new/izumitelno/p1", headers=headers)
html = BS(r.content, 'html.parser')

for el in html.select(".items > .article-summary"):
    title = el.select('.caption > a')
    if title:  # Это условие нужно, чтобы избежать ошибок, если элемент не найден
        print(title[0].text)
