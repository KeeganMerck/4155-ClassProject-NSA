from flask import Blueprint, request, redirect, session, flash, render_template

from models.models import db, User

router = Blueprint('main', __name__, template_folder='templates')

@router.get('/')
def default():
    return redirect('/login')

@router.get('/create_account')
def create_account_page():
    return render_template('accountcreation.html')

@router.post('/create_account')
def create_account():
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

@router.get('/login')
def login_page():
    return render_template('login.html')

@router.post('/login')
def login():
    username = request.form['username']
    #query for username in the db
    user = User.query.filter_by(username=username).first()
    #if username is good then go to next step
    if user:
        session['user'] = user.username

        #If the username is good then we go to the next step in the login process which is image upload for face recognition
    return redirect("/upload", code=302)

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