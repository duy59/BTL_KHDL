import asyncio
from bs4 import BeautifulSoup
from utils.helper import slugify

async def process_detail_html(domain, html):
    soup = BeautifulSoup(html, 'html.parser')
    description = soup.find('meta', {'name': 'description'})['content']
    title = ''
    raw_content = ''
    category = {}
    author = ''

    if domain == 'vneconomy.vn':
        title = soup.find('h1', {'class': 'detail__title'}).get_text()
        raw_content = soup.find('div', {'class': 'detail__content'}).decode_contents()
        cat = soup.find('h1', {'class': 'category-main'}).get_text()
        category = {
            'name': cat,
            'slug': slugify(cat)
        }
        author = soup.find('div', {'class': 'detail__author'}).get_text()
    elif domain == 'cafef.vn':
        title = soup.find('h1', {'class': 'title'}).get_text()
        raw_content = soup.find('div', {'class': 'w640'}).decode_contents()
        cat = soup.find('a', {'class': 'category-page__name cat'}).get_text()
        category = {
            'name': cat,
            'slug': slugify(cat)
        }
        author = soup.find('p', {'class': 'author'}).get_text()
        if author == '':
            author = soup.find('div', {'class': 'sevenPostAuthor'}).get_text()
        author = author.replace('Theo ', '')
    elif domain == 'vnexpress.net':
        title = soup.find('h1', {'class': 'title-detail'}).get_text()
        tmp_content = soup.find('p', {'class': 'description'}).get_text()
        raw_content = soup.find('div', {'class': 'fck_detail'}).decode_contents()
        raw_content = tmp_content + "<br>" + raw_content
        cat = soup.find('ul', {'class': 'breadcrumb'}).find('a').get('title')
        category = {
            'name': cat,
            'slug': slugify(cat)
        }
        author = soup.find('div', {'class': 'box-tinlienquanv2'}).find_next('strong').get_text()
    elif domain == 'vov.vn':
        title = soup.find('h1', {'class': 'article-title'}).get_text()
        raw_content = soup.find('div', {'class': 'article-content text-long'}).decode_contents()
        cat = soup.find('div', {'class': 'breadcrumb-item'}).find_all('a')[-1].get_text()
        category = {
            'name': cat,
            'slug': slugify(cat)
        }
        author = soup.find('div', {'class': 'article-author'}).find('a').get_text()

    return {
        'title': title,
        'raw_content': raw_content,
        'description': description,
        'category': category,
        'author': author
    }

# Example usage
# html_content = "<html>...</html>"
# result = asyncio.run(process_detail_html('vneconomy.vn', html_content))