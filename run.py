import json
import requests
import time
import traceback

from parsers import get_clien_deals, get_ppomppu_deals, get_ruliweb_deals


WEBHOOK_PATH = 'webhooks.json'
SITES = {
    'clien': {
        'url': 'https://www.clien.net/service/board/jirum',
        'parser': get_clien_deals
    },
    'ruliweb': {
        'url': 'https://bbs.ruliweb.com/market/board/1020',
        'parser': get_ruliweb_deals
    },
    'ppomppu': {
        'url': 'http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu',
        'parser': get_ppomppu_deals
    }
}


with open(WEBHOOK_PATH, 'r') as f:
    webhook_urls = json.load(f)


def crawl_all():
    for name, info in iter(SITES.items()):
        print(f'Crawling {name}...')
        url = info['url']
        parser = info['parser']

        deals = parser(name, url)

        deal_count = len(deals)
        if len(deals) > 0:
            print(f'    {deal_count} deals found!')
        else:
            print(f'    No deals found.')

        for webhook_url in webhook_urls:
            for deal in deals:
                text = f"{deal['title']}\n{deal['url']}"
                send_webhook(webhook_url, text)


def send_webhook(url, text, channel=None):
    data = {'text': text}
    if channel:
        data['channel'] = channel

    try:
        requests.post(
            url,
            data=json.dumps(data),
            headers={'Content-Type': 'application/json'}
        )
    except Exception:
        tb = traceback.format_exc()
        print(tb)


if __name__ == '__main__':
    try:
        while True:
            crawl_all()
            time.sleep(60)
    except KeyboardInterrupt:
        print('Goodbye!')

