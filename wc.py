# -*- encoding: utf-8 -*-
import os
import pdb
import shelve
import webbrowser

import imapy
from imapy.query_builder import Q
from more_itertools import chunked

HOST = os.environ['WC_HOST']
USERNAME = os.environ['WC_USERNAME']
PASSWORD = os.environ['WC_PASSWORD']


box = imapy.connect(
    host=HOST,
    username=USERNAME,
    password=PASSWORD,
    ssl=True,
)

q = Q()

emails = box.folder('INBOX').emails(
    q.sender("pycoders.com")
)
DONE_FOLDER = 'weekly' + box.separator + '1'

if DONE_FOLDER not in box.folders():
    base, sub = DONE_FOLDER.split(box.separator)
    box.make_folder(base)
    box.folder(base).make_folder(sub)

print(box.folders())

with shelve.open('wc.db', writeback=True) as db:
    if 'emails' not in db:
        db['emails'] = {}
    if 'links' not in db:
        db['links'] = set()


with shelve.open('wc.db', writeback=True) as db:
    for email in emails:
        db['emails'][email['subject']] = {
            'headers': email['headers'],
            'from': email['from'],
            'from_email': email['from_email'],
            'from_whom': email['from_whom'],
            'to': email['to'],
            'flags': email['flags'],
            'subject': email['subject'],
            'cc': email['cc'],
            'date': email['date'],
            'text_normalized': email['text'][0]['text_normalized'],
        }


for email in emails:
    email.move(DONE_FOLDER)

def parse_links(text):
    for line in text.split('('):
        maybe_link = line.split(')')[0]
        if maybe_link.startswith('http'):
            yield maybe_link

def is_unsubscribe(link):
    return 'unsubscribe' in link

def is_instapaper(link):
    return link.startswith('http://www.instapaper.com/')

def is_tw_action(link):
    return link.startswith('http://twitter.com/intent/tweet')


with shelve.open('wc.db', writeback=True) as db:
    for subject, email in db['emails'].items():
        links = set(parse_links(email['text_normalized']))
        for email in emails:
            db['links'].update(set(links))



with shelve.open('wc.db') as db:
    for chunk in chunked(db['links'], 7):  # XXX: 7 is magic ;)
        for link in chunk:
            if (not is_tw_action(link) and not is_instapaper(link) 
                and not is_unsubscribe(link)):
                webbrowser.open_new_tab(link)

        con = input('Next batch (Y/n)')
        if con.lower().startswith('n'):
            break
