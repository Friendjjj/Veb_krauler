from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup

# Интерфейс краулера
class Crawler(ABC):
    @abstractmethod
    def crawl(self, url: str) -> None:
        pass

# Интерфейс парсера
class Parser(ABC):
    @abstractmethod
    def parse(self, content: str) -> list:
        pass

# Реализация конкретного краулера
class SimpleCrawler(Crawler):
    def __init__(self, parser: Parser):
        self.parser = parser

    def crawl(self, url: str) -> list:
        response = requests.get(url)
        print(response.status_code)
        print(response.text[:500])  # Показать первые 500 символов содержимого страницы

        return self.parser.parse(response.text)

# Реализация парсера для стихов
class StihiParser(Parser):
    def parse(self, content: str) -> list:
        soup = BeautifulSoup(content, 'html.parser')
        poems = soup.find_all(class_='poem-link')
        return [poem.text for poem in poems]

# Декоратор для прокси
class ProxyCrawlerDecorator(Crawler):
    def __init__(self, crawler: Crawler, proxy: str):
        self.crawler = crawler
        self.proxy = proxy

    def crawl(self, url: str) -> list:
        # Здесь можно добавить логику использования прокси
        return self.crawler.crawl(url)

# Код для исполнения
if __name__ == "__main__":
    # Создание объекта парсера и краулера
    parser = StihiParser()
    crawler = SimpleCrawler(parser)

    # Декорирование краулера для использования прокси (если нужно)
    # proxy = "http://my-proxy:8080"
    # proxy_crawler = ProxyCrawlerDecorator(crawler, proxy)
    # Запуск краулера с прокси
    # poems = proxy_crawler.crawl("https://www.stihi.ru/avtor/akutagava")

    # Запуск краулера без прокси
    poems = crawler.crawl("https://www.stihi.ru/avtor/akutagava")
    for poem in poems:
        print(poem)
