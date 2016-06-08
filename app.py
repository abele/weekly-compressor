import shelve

from flask import Flask, render_template_string

app = Flask('weekly-compressor')


@app.route('/')
def index():
    tmpl = """<html><body>
        <ul>
        {% for link in links.values() %}
            <li><a href="{{ link.url }}">{{ link.title }}</a></li>
        {% endfor %}
        </ul>
    </body></html>"""
    with shelve.open('wc.db') as db:
        resp = render_template_string(tmpl, links=db['rich_links'])

    return resp


if __name__ == '__main__':
    app.run()
