from flask import Flask

app = Flask(__name__)

from routes.stackRoutes import stack_blueprint
app.register_blueprint(stack_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
