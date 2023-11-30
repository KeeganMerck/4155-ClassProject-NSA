from flask import Blueprint, request, redirect, session, flash, render_template, jsonify

from models.models import db, User
from checkSesh import checkPage
router = Blueprint('main', __name__, template_folder='templates')

@router.get('/')
def default():
    return redirect('/login')

@router.route('/create_account', methods=['GET', 'POST'])
def create_account():
    
    session['redire'] = '/create2'
    session['flag'] = 0
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        imagecategory = request.form['imagecategory']
        print("HEY")
        user = User(username=username, name=name, email=email, imagecategory=imagecategory)
        print("HEY")
        session['currentUser'] = user.username
        print("HEY")
        db.session.add(user)
        db.session.commit()

        flash("Account Information taken")
        return redirect("/create2")
    return render_template('accountcreation.html')

@router.get('/login')
def login_page():
    session['corVal'] = 0
    session['location']=1
    return render_template('login.html')


@router.post('/login')
def login():
    
    username = request.form['username']
    #query for username in the db
    user = User.query.filter_by(username=username).first()
    #if username is good then go to next step
    if user:
        session['username'] = user.username
    if session.get('location') != None and checkPage(session.get('location'),1) >= 1:
        print("hey")
        session['location'] = 2
        #If the username is good then we go to the next step in the login process which is image upload for face recognition
        return redirect("/upload", code=302)
    else:
        print("whats up")
        return redirect("/login", code = 200)

#Authentication successful page
@router.get('/home_page')
def success():
    return render_template('home_page.html')

@router.get('/delete_all_users')
def delete_all_users():
    try:
        # Use SQLAlchemy to delete all rows in the User table
        db.session.query(User).delete()
        db.session.commit()
        flash("All users have been deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Failed to delete all users: {str(e)}", "error")
    return redirect("/login")

@router.get('/delete_all_sessions')
def delete_all_sessions():
    try:
        # Use SQLAlchemy to delete all rows in the User table
        session.clear()
        flash("All users have been deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash((f"Failed to delete all sessions: {str(e)}", "error"))
    return redirect("/create_account")



    