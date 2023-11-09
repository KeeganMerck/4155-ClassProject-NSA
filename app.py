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


from flask import Flask, request, session, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from blueprints.image_grid import router as image_router
import requests
from modifedFacereco import loginFace
import re
from werkzeug.datastructures import FileStorage

# init app variable
app = Flask(__name__)
usernameDict = {}
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

@app.route('/')
def default():
    return redirect('/login')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        imagecategory = request.form['imagecategory']

        user = User(username=username, name=name, email=email, imagecategory=imagecategory)
        session['currentUser'] = user.username
        db.session.add(user)
        db.session.commit()

        flash("Account Information taken")
        return redirect("/create2")
    return render_template('accountcreation.html')


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  name = db.Column(db.String(120), nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  imagecategory = db.Column(db.String(50), nullable=False)
  image_path = db.Column(db.String(255))
  #login route
  #route for login in
  
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        #query for username in the db
        user = User.query.filter_by(username=username).first()
        #if username is good then go to next step
        if user:
            usernameDict["username"] = user
   
            #If the username is good then we go to the next step in the login process which is image upload for face recognition
        return redirect("/upload", code=302)
    return render_template('login.html')

#For face Reco
#put your face in with the capture and test it with the flask app
#you gotta click caputre, then wait 10 seconds then click upload. Thes ensure taht hte porcessing is complete before
#chcking you, Will be fixed in next ssprint
#You can prolly check with joe but you will need to change the lin 116 to set middle var of the login function to the string of my picture
#Me and crow tapped in like morse code



@app.route('/upload', methods=['POST', 'GET'])
def upload_image():
    #on post request:
    if request.method == 'POST':
        #get the image
        image = request.files['image']
    #if there is an image then 
        if image:
            #save the image
            image.save('uploads/captured-image.png')
            #see if image is loginable
            if loginFace(0, 'uploads/captured-image.png', usernameDict["username"].username) == 1:
                print("got here")
                session['corVal'] = 1     
            else:
                session['corVal'] = 0
            # Save the image to the "uploads" folder
    #if the image iis elog inable then and matches the users face then redirect them to the next pge
        if session.get('corVal') == 1:
            flash("Face Recognized", "success")
            return redirect("/image_grid")
        else:
            #redirect them to the failed page
            flash("Face could not be recognized", "error")
            return redirect("/login")
    return render_template('camcam.html')

#CHANGE NAME OF THIS WACK ASS BO
@app.route('/create2', methods=['POST', 'GET'])
def uploadTestImages():
    #on post request:
    if request.method == 'POST':
        print(session['currentUser'])
        
        #get the image
        image = request.files['image']
       
        if image:
            #save the image
            paths = "test/"+str(session['currentUser'])
            pathe = os.path.exists(paths)
            if not pathe:

            # Create a new directory because it does not exist
                os.makedirs(paths)
                print("The new directory is created!")
            image.save(str(paths)+"/"+str(session['currentUser'])+ image.filename)
           
            flash("Account Created Successfully")
    #if there is an image then 
           
            # Save the image to the "uploads" folder
    #if the image iis elog inable then and matches the users face then redirect them to the next pge
        
    return render_template('testPhotos.html')

#Chat gpt bullish 
        
