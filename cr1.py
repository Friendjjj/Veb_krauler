import requests
from bs4 import BeautifulSoup
import os

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

def get_authors(url):
    content = get_page_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all('a', class_='recomlink')
    return [('https://stihi.ru' + link['href'], link.text) for link in links]

def get_poems(author_url):
    content = get_page_content(author_url)
    soup = BeautifulSoup(content, 'html.parser')
    links = soup.find_all('a', class_='poemlink')
    return ['https://stihi.ru' + link['href'] for link in links]

def save_poem(poem_url, author_folder):
    content = get_page_content(poem_url)
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.find('h1').text.strip()
    poem = soup.find('div', class_='text').text.strip()
    file_path = os.path.join(author_folder, f"{title}.txt")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(poem)

def web_crawler(start_url):
    authors = get_authors(start_url)
    for author_url, author_name in authors:
        author_folder = os.path.join('Authors', author_name)
        os.makedirs(author_folder, exist_ok=True)

        poems = get_poems(author_url)
        for poem_url in poems:
            save_poem(poem_url, author_folder)
            

start_url = 'https://stihi.ru/authors/editor.html?year=2023&month=11&day=8'
web_crawler(start_url)
