from flask import Flask

app = Flask(__name__)

from app.routes.stacksRoutes import post_blueprint
app.register_blueprint(post_blueprint)
