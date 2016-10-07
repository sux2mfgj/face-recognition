from flask import Flask, send_file

app = Flask(__name__)


@app.route('/image')
def get_image():
    return send_file('./test.jpg', mimetype='image/jpg')


if __name__ == "__main__":
    app.run()
