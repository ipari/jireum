import json
import requests

from bs4 import BeautifulSoup
from urllib.parse import parse_qsl


SAVE_PATH = 'jireum.json'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57'}


class LastArticleIDs(object):
    def __init__(self, path):
        self.path = path
        self.info = self.load_info()

    def load_info(self):
        try:
            with open(self.path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get(self, name):
        return int(self.info.get(name, 0))

    def set(self, name, article_id):
        self.info[name] = article_id
        with open(self.path, 'w') as f:
            json.dump(self.info, f)


last_article_ids = LastArticleIDs(SAVE_PATH)


def get_soup(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f'[Error] Failed to request: {url}')
        return
    return BeautifulSoup(response.text, features='html.parser')


def process_deals(name, deals):
    if len(deals) > 0:
        deals.reverse()
        last_article_id = deals[-1]['article_id']
        last_article_ids.set(name, last_article_id)
    return deals


def get_clien_deals(name, url):
    soup = get_soup(url)
    if soup is None:
        return []

    deals = []
    last_article_id = last_article_ids.get(name)
    links = soup.findAll('a', {'data-role': 'list-title-text'})

    for link in links:
        # '/service/board/jirum/13755650?od=T31&po=0&category=&groupCd='
        rel_link = link.get('href')
        article_id = int(rel_link.split('/')[-1].split('?')[0])
        title = link.text
        title = title.replace('\n', '').replace('\t', '')

        if article_id <= last_article_id:
            break

        deals.append({
            'url': f'{url}/{article_id}',
            'title': title,
            'article_id': article_id
        })

    return process_deals(name, deals)


def get_ruliweb_deals(name, url):
    soup = get_soup(url)
    if soup is None:
        return []

    # 테이블에서 공지사항을 제거한다.
    for tr in soup.findAll('tr', {'class': 'table_body'}):
        if 'inside' in tr['class']:
            tr.decompose()

    deals = []
    last_article_id = last_article_ids.get(name)
    tds = soup.findAll('td', {'class': 'subject'})

    for td in tds:
        link = td.find('a')

        # url 마지막에 붙은 '?'를 뗴어준다.
        url = link.get('href')[:-1]
        article_id = int(url.split('/')[-1])
        title = link.text

        if article_id <= last_article_id:
            break

        deals.append({
            'url': url,
            'title': title,
            'article_id': article_id
        })

    return process_deals(name, deals)


def get_ppomppu_deals(name, url):
    soup = get_soup(url)
    if soup is None:
        return []

    deals = []
    last_article_id = last_article_ids.get(name)
    trs = soup.findAll('tr', {'class': ['list0', 'list1']})

    for tr in trs:
        link = tr.find('table').findAll('a')[1]

        title = link.find('font').text
        rel_path = link.get('href')
        query = dict(parse_qsl(rel_path))
        article_id = int(query['no'])

        if article_id <= last_article_id:
            break

        deals.append({
            'url': f'{url}&no={article_id}',
            'title': title,
            'article_id': article_id
        })

    return process_deals(name, deals)
