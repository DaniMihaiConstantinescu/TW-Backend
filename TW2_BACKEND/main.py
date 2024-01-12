from flask import Flask
import logging

app = Flask(__name__)

from routes.stackRoutes import stack_blueprint
app.register_blueprint(stack_blueprint)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        logging.exception("An error occurred: %s", e)
