import shelve

import wc
from flask import Flask, Markup, render_template_string

app = Flask('weekly-compressor')


@app.route('/')
def index():
    tmpl = """<html><body>
        <ul>
        {% for link in links %}
            <li><a href="{{ link }}">{{ link }}</a></li>
        {% endfor %}
        </ul>
    </body></html>"""
    checks = [
        wc.is_instapaper,
        wc.is_tw_action,
        wc.is_unsubscribe,
    ]
    with shelve.open('wc.db') as db:
        links = (link for link in db['links'] 
                 if not any(check(link) for check in checks))
        resp = render_template_string(tmpl, links=links)

    return resp


if __name__ == '__main__':
    app.run()
