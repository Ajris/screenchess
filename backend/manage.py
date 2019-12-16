from flask import Flask

app = Flask(__name__)


@app.route('/show-position/<str:fen>')
def show_position(fen):
    return fen


if __name__ == '__main__':
    app.run()
