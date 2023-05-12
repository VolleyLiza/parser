import requests
from bs4 import BeautifulSoup as BS 
import csv

HOST = 'https://tsn.ua/'
URL = 'https://tsn.ua/keywords/ozbroyennya-ta-armiya'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r.text

def get_content(html):
    soup = BS(html, 'html.parser')
    items = soup.find_all('div', class_='c-card__body')
    posts = []

    for item in items:
        title = item.find('h3', class_='c-card__title')
        link_product = title.find('a').get('href')
        category = item.find('footer', class_='c-card__category').get_text()
        link_category = item.find('footer', class_='c-card__category').find('a').get('href')

        posts.append({
            'title': title.get_text(strip=True),
            'link_product': link_product if link_product.startswith('http') else HOST + link_product,
            'category': category.strip(),
            'link_category': link_category if link_category.startswith('http') else HOST + link_category
        })

    return posts

def save_csv(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Заголовок', 'Посилання на товар', 'Категорія', 'Посилання на категорію'])
        for item in items:
            writer.writerow([item['title'], item['link_product'], item['category'], item['link_category']])

def main():
    html = get_html(URL)
    if html:
        posts = get_content(html)
        save_csv(posts, 'tsn.csv')
        print('Збережено!')
    else:
        print('Помилка отримання HTML-сторінки')

if __name__ == '__main__':
    main()
