# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, flash

from grab import Grab


app = Flask(__name__)
app.secret_key = 'the random string'


@app.route('/', methods=['POST', 'GET'])
def index():
    """главная страница"""
    if request.method == 'POST':
        url = request.form['url']
        if url != '':
            parser = Grab(url)
            images = parser.run()
            if 'Ошибка' in images:
                flash(images, 'error')
                return render_template('index.html')
            return render_template("gallery.html", images=images)
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    """404 page"""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
