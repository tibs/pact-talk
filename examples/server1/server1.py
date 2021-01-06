#!/usr/bin/env python3

from bottle import Bottle

app = Bottle()

@app.route('/butter/<substrate>')
def butter(substrate):
    return f'{substrate} and butter'

if __name__ == '__main__':
    app.run()
