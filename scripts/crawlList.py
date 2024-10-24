import asyncio
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from utils.crawl import crawl_post
from .processListHtml import process_list_html

max_page = 5
urls = []
links = []

async def crawl_list(url):
    global urls, links
    url_source = urlparse(url)
    hostname = url_source.hostname
    raw_html = await crawl_post(url)
    
    if hostname == 'cafeland.vn':
        soup = BeautifulSoup(raw_html, 'html.parser')
        list_items = soup.select('.list-type-14 h3 a')
        for element in list_items:
            urls.append(element['href'])
        
        pagi = soup.select('.nav-paging a[title="Trang cuối"]')
        for _ in pagi:
            for i in range(2, max_page + 1):
                links.append(f"{url}page-{i}")
        
        for link in links:
            raw_html_pagi = await crawl_post(link)
            soup_pagi = BeautifulSoup(raw_html_pagi, 'html.parser')
            list_pagi = soup_pagi.select('.list-type-14 h3 a')
            for element in list_pagi:
                urls.append(element['href'])
    else:
        data = await process_list_html(hostname, raw_html, 1)
        urls.extend(data['urls'])
        if data['next_pages']:
            for link in data['next_pages']:
                raw_html_pagi = await crawl_post(link)
                page_next = 1
                data_pagi = await process_list_html(hostname, raw_html_pagi, page_next)
                if data_pagi['urls']:
                    urls.extend(data_pagi['urls'])
    
    return urls

# Example usage
# asyncio.run(crawl_list('https://example.com'))