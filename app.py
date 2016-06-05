import shelve

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

    with shelve.open('wc.db') as db:
        resp = render_template_string(tmpl, links=db['links'])

    return resp


if __name__ == '__main__':
    app.run()
