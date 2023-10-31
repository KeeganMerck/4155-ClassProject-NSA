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
# 2)  go to http://localhost:5000/create_account
# 
# 3) fill out form then submit
# 
# 4) view values in terminal window or 4155User.db

from flask import Flask
from flask import render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from blueprints.image_grid import router as image_router

# init app variable
app = Flask(__name__)

# init secret key
app.secret_key = 'your_secret_key'

# Set database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///4155User.db'

# init db variable
db = SQLAlchemy(app)

# init SQLAlchemy instance
migrate = Migrate(app, db)

# calling of image grid blueprints to handle routes
app.register_blueprint(image_router)

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        imagecategory = request.form['imagecategory']

        user = User(username=username, name=name, email=email, imagecategory=imagecategory)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('success'))
    return render_template('accountcreation.html')

@app.route('/success')
def success():
    return 'Account created successfully!'


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  name = db.Column(db.String(120), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  imagecategory = db.Column(db.String(50), nullable=False)
  image_path = db.Column(db.String(255))
  