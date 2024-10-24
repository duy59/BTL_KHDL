import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
                                
import asyncio
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.crawl import crawl_post
from utils.helper import slugify
from processDetailHtml import process_detail_html

blog_posts = []

async def create_blog_post(data):
    slug = data.get('slug')
    existing_blog_post = next((post for post in blog_posts if post['slug'] == slug), None)
    if existing_blog_post:
        return {'error': 'Slug already exists'}
    blog_posts.append(data)
    return data

async def get_single_blog_post_by_condition(condition={}):
    blog_post = next((post for post in blog_posts if all(post.get(key) == value for key, value in condition.items())), None)
    if not blog_post:
        return {'status': False, 'error': 'Blog post not found'}
    return {'status': True, 'blog_post': blog_post}

async def crawl_detail(url, update=0):
    condition = {'url_origin': url}
    try:
        url_source = urlparse(url)
        hostname = url_source.hostname
        if update == 0:
            info = await get_single_blog_post_by_condition(condition)
            if info['status']:
                return info['status']
        
        raw_html = await crawl_post(url)
        blog = {}
        if hostname == 'cafeland.vn':
            soup = BeautifulSoup(raw_html, 'html.parser')
            title = soup.find('h1').get_text()
            body_html = soup.find(id='sevenBoxNewContentInfo')
            for tag in body_html(['script', 'input', 'form', 'style', '.box-thaoluan']):
                tag.decompose()
            raw_content = str(body_html)
            description = soup.find('meta', {'name': 'description'})['content']
            category = {
                'name': 'Tài chính - Chứng khoán',
                'slug': 'tai-chinh'
            }
            slug = slugify(title)
            author = soup.find('p', {'class': 'author'}).get_text()
            if not author:
                author = soup.find(class_='sevenPostAuthor').get_text()
            if update == 1:
                return {
                    'title': title.strip(),
                    'slug': slug,
                    'description': description,
                    'content': raw_content,
                    'url_origin': url,
                    'category': category,
                    'author': author,
                    'type': 'crawl'
                }
            blog = await create_blog_post({
                'title': title.strip(),
                'slug': slug,
                'description': description,
                'content': raw_content,
                'url_origin': url,
                'category': category,
                'author': author,
                'type': 'crawl'
            })
        else:
            data = await process_detail_html(hostname, raw_html)
            slugified_title = slugify(data['title'])
            if update == 1:
                return {
                    'title': data['title'].strip(),
                    'slug': slugified_title,
                    'description': data['description'],
                    'content': data['raw_content'],
                    'url_origin': url,
                    'category': data['category'],
                    'author': data['author'],
                    'type': 'crawl'
                }
            blog = await create_blog_post({
                'title': data['title'].strip(),
                'slug': slugified_title,
                'description': data['description'],
                'content': data['raw_content'],
                'url_origin': url,
                'category': data['category'],
                'author': data['author'],
                'type': 'crawl'
            })
        return blog
    except Exception as error:
        return True

# Example usage
# asyncio.run(crawl_detail('https://example.com', 0))