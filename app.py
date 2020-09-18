from configuration import Config
from flask import Flask
from flask import jsonify
from pymongo import errors

from packages_learning.auth.auth import auth_bp
from packages_learning.content.vocabulary import vocab_bp

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth_bp)
app.register_blueprint(vocab_bp)


@app.errorhandler(errors.ServerSelectionTimeoutError)
def pymongo_error(error):
    response = jsonify({
        "code"  : 500,
        "msg"   : "Connection Failed, Mongodb refuse to connect"
    }), 500
    return response


if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0", debug=True)
