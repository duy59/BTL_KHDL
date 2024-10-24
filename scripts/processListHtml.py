from bs4 import BeautifulSoup

async def process_list_html(domain, html, page_next=0):
    soup = BeautifulSoup(html, 'html.parser')
    urls = []
    next_pages = []

    if domain == 'vneconomy.vn':
        for element in soup.select('article.story--featured.story--timeline'):
            url = element.select_one('h3.story__title a')['href']
            urls.append(f"https://vneconomy.vn{url}")
        if page_next == 1:
            for element in soup.select('li.page-item'):
                link = element.select_one('a')
                if link.text != '1':
                    url = element.select_one('a')['href']
                    next_pages.append(f"https://vneconomy.vn{url}")
    elif domain == 'cafef.vn':
        if page_next == 1:
            for element in soup.select('.box-category-item'):
                url = element.select_one('h3 a')['href']
                urls.append(f"https://cafef.vn{url}")
        else:
            for element in soup.select('div.listchungkhoannew .box-category-item'):
                url = element.select_one('h3 a')['href']
                urls.append(f"https://cafef.vn{url}")
            id = soup.select_one('#hdZoneId')['value']
            for i in range(2, 6):
                next_pages.append(f"https://cafef.vn/timelinelist/{id}/{i}.chn")
    elif domain == 'vnexpress.net':
        for element in soup.select('.list-news-subfolder article.item-news.item-news-common.thumb-left'):
            url = element.select_one('h3 a')['href']
            urls.append(url)
        if page_next == 1:
            url = soup.select_one('meta[property="og:url"]')['content']
            for i in range(2, 6):
                next_pages.append(f"{url}-p{i}")
    elif domain == 'vov.vn':
        for element in soup.select('.row.test .article-card'):
            url = element.select_one('a.vovvn-title')['href']
            urls.append(f"https://vov.vn{url}")
        if page_next == 1:
            url = soup.select_one('link[rel=canonical]')['href']
            for i in range(2, 6):
                next_pages.append(f"{url}?page={i}")

    return {'urls': urls, 'next_pages': next_pages}

# Example usage
# html_content = "<html>...</html>"
# result = asyncio.run(process_list_html('vneconomy.vn', html_content))