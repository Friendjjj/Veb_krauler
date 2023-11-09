import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

# Стратегия для выполнения HTTP-запросов
class HttpRequestStrategy(ABC):

    @abstractmethod
    def fetch(self, url: str) -> str:
        pass

class DirectRequest(HttpRequestStrategy):

    def fetch(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text

class ProxyRequest(HttpRequestStrategy):

    def __init__(self, proxy: str):
        self.proxy = proxy

    def fetch(self, url: str) -> str:
        proxies = {
            "http": self.proxy,
            "https": self.proxy
        }
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        return response.text

class WebCrawler:

    def __init__(self, strategy: HttpRequestStrategy):
        self.strategy = strategy

    def fetch_data(self, url: str) -> str:
        return self.strategy.fetch(url)

    def fetch_poems(self, author_url: str) -> list:
        poems = []

        html = self.fetch_data(author_url)
        print(html[:500])

        soup = BeautifulSoup(html, 'html.parser')

        # Ищем блоки стихов на странице автора
        poem_blocks = soup.select('.poem')

        for block in poem_blocks:
            poem_text = block.get_text(separator='\n').strip()
            poems.append(poem_text)

        return poems

# Пример использования
try:
    crawler = WebCrawler(DirectRequest())
    poems = crawler.fetch_poems("https://stihi.ru/avtor/authorname")

    for poem in poems:
        print(poem)
        print("-" * 50)
except Exception as e:
    print(f"Ошибка: {e}")


# Чтобы использовать прокси:
# proxy = "http://your_proxy_address:port"
# crawler = WebCrawler(ProxyRequest(proxy))
