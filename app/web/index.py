from flask import Flask, request, render_template, Response
from datetime import datetime
from flask import jsonify

from app.parser.Parser import Parser

app = Flask(__name__, static_url_path='',
            static_folder='static',
            template_folder='templates')


@app.route('/')
def index():
    if request.method == 'GET':
        return render_template('index.html')
    return '<html><body><h1>Method not supported</h1></body></html>'


@app.route('/parse', methods=['POST'])
def parse():
    if request.method == 'POST':
        amount = request.get_json().get('amount', 5)
        parser = Parser()
        data = parser.get_petitions(amount)[:amount + 1]
        filename = f'reports/data-{datetime.now().strftime("%m-%d-%y")}.csv'
        with open(filename, 'w') as f:
            for piece in data:
                try:
                    f.write(piece.serialize())
                # если названия полей
                except AttributeError:
                    f.write(piece + '\n')
        return jsonify({'filename': filename})


@app.route('/reports/<filename>', methods=['GET'])
def get_report(filename):
    with open('reports/' + filename, 'r') as f:
        data = f.read()
    return Response(data, mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)
