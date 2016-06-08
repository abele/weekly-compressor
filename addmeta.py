import shelve

import wc
from bs4 import BeautifulSoup as BS
import requests


checks = [
    wc.is_instapaper,
    wc.is_tw_action,
    wc.is_unsubscribe,
]

with shelve.open('wc.db', writeback=True) as db:
    if 'rich_links' not in db:
        db['rich_links'] = {}

    for link in db['links'] :
        if not any(check(link) for check in checks):
            resp = requests.get(link)
            soup = BS(resp.text, 'html.parser')
            db['rich_links'][link] = {
                'url': link,
                'title': soup.title.text,
            }
            db.sync()
