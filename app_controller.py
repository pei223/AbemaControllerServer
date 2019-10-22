# Flask などの必要なライブラリをインポートする
from flask import Flask
from config import Config
from abema_controller import AbemaController

app = Flask(__name__)


@app.route('/switch', methods=['GET'])
def switch():
    AbemaController.instance().switch()
    return {'message': 'Success'}, 200

@app.route('/channel_next', methods=['GET'])
def channel_next():
    AbemaController.instance().channel_next()
    return {'message': 'Success'}, 200


@app.route('/channel_prev', methods=['GET'])
def channel_prev():
    AbemaController.instance().channel_prev()
    return {'message': 'Success'}, 200


@app.route('/full_screen', methods=['GET'])
def full_screen():
    AbemaController.instance().toggle_full_screen()
    return {'message': 'Success'}, 200


if __name__ == '__main__':
    config = Config.instance()
    app.run(host=config.ip_address, port=config.port)
