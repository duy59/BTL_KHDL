import sys
import os
import asyncio
import json
from scripts.crawlDetail import crawl_detail
from scripts.crawlList import crawl_list

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def main():
    list_cat = [
        'https://vneconomy.vn/chung-khoan.htm',
        ''
    ]

    all_data = []

    for cat in list_cat:
        urls = await crawl_list(cat)
        print(urls)
        for url in urls:
            data = await crawl_detail(url)
            all_data.append(data)

    with open('crawledData.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    try:
        asyncio.run(main())
        print('Done')
    except Exception as error:
        print('Error:', error)
        exit(1)