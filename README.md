# Veb_krauler
import requests
from bs4 import BeautifulSoup
import abc
# Определяем интерфейс для стратегии скачивания страницы
class PageFetcherStrategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch(self, url: str) -> str:
        pass
# Реализация стратегии скачивания страницы напрямую
class DirectPageFetcher(PageFetcherStrategy):
    def fetch(self, url: str) -> str:
        response = requests.get(url)
        return response.text
# Реализация стратегии скачивания страницы через прокси
class ProxyPageFetcher(PageFetcherStrategy):
    def fetch(self, url: str) -> str:
        proxies = {"http": "http://your_proxy_here", "https": "https://your_proxy_here"}
        response = requests.get(url, proxies=proxies)
        return response.text
# Класс краулера
class Crawler:
    def __init__(self, fetcher_strategy: PageFetcherStrategy):
        self.fetcher_strategy = fetcher_strategy
    def crawl(self, url: str) -> None:
        page_content = self.fetcher_strategy.fetch(url)
        self.parse_page(page_content)
    def parse_page(self, page_content: str) -> None:
        soup = BeautifulSoup(page_content, 'html.parser')
        poems = soup.find_all('div', class_='text')
        for idx, poem in enumerate(poems):
            print(f"Poem {idx+1}:\n{poem.text}\n{'-'*20}")
# Алгоритм запуска краулера
if __name__ == "__main__":
    url = "https://stihi.ru/poemslist.html"  # URL для сбора данных
    # Выбор стратегии скачивания: DirectPageFetcher или ProxyPageFetcher
    fetcher_strategy = DirectPageFetcher()
    # Создаем экземпляр краулера и запускаем его
    crawler = Crawler(fetcher_strategy)
    crawler.crawl(url)

