from flask import Flask
from blueprints.image_grid import router as image_router

app = Flask(__name__)

app.secret_key = 'your_secret_key'

app.register_blueprint(image_router)