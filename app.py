# python application to support Flask-SQLAlchemy backend for project
# Libraries:
# Flask
# SQLAlchemy
# Flask_SQLAlchemy
# Flask-Migrate
# 
# How to test:
# 
# 1)  Run in terminal with `flask run` 
# 
# 2)  go to http://localhost:5000
# 
# 3) fill out form then submit
# 
# 4) view values in terminal window or 4155User.db

from flask import Flask
from flask_migrate import Migrate

from models.models import db

from blueprints.image_grid import router as image_router
from blueprints.main_blueprint import router as main_router
from blueprints.face_reco_blueprint import router as face_reco_router

#APP INIT
app = Flask(__name__)
app.secret_key = 'your_secret_key'

#DATABASE INIT
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///4155User.db'
db.init_app(app)
migrate = Migrate(app, db)

# registering of blueprints
app.register_blueprint(main_router)
app.register_blueprint(image_router)
app.register_blueprint(face_reco_router)


