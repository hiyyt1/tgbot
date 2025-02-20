# dream_parser.py

import requests
from bs4 import BeautifulSoup


cookies = {
    'gnezdo_uid': '19524cf3e45c3b90dd0468eb',
    '_gid': 'GA1.2.2054445265.1740079317',
    '_ga_EPBRFBH6TX': 'GS1.1.1740079317.1.1.1740079416.0.0.0',
    '_ga': 'GA1.1.98022133.1740079317',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en;q=0.9,cy;q=0.8',
    'priority': 'u=0, i',
    'referer': 'https://my-calend.ru/sonnik?search=%D0%BB%D0%BE%D1%81%D0%BE%D1%81%D1%8C',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "YaBrowser";v="25.2", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36',
}


def search_dream(text):
    params = {'search': text}
    response = requests.get('https://my-calend.ru/sonnik', params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for item in soup.find_all('h3'):
        link_tag = item.find('a')
        if link_tag:
            title = link_tag.text
            link = link_tag['href']
            description_tag = item.find_next('p')
            description = description_tag.text if description_tag else "Описание отсутствует"
            results.append({
                'title': title,
                'link': link,
                'description': description
            })
    return results
