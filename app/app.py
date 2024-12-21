from flask import Flask
from .routes import my_blueprint

app = Flask(__name__)

# Blueprintを登録
app.register_blueprint(my_blueprint)
