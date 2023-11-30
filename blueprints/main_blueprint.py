from flask import Blueprint, request, redirect, session, flash, render_template, jsonify

from models.models import db, User

router = Blueprint('main', __name__, template_folder='templates')

@router.get('/')
def default():
    return redirect('/login')

@router.route('/create_account', methods=['GET', 'POST'])
def create_account():
    session['flag'] = 0
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        imagecategory = request.form['imagecategory']
        user = User(username=username, name=name, email=email, imagecategory=imagecategory)
        session['currentUser'] = user.username
        db.session.add(user)
        db.session.commit()

        flash("Account Information taken", "success")
        return redirect("/create2")
    return render_template('accountcreation.html')

@router.get('/login')
def login_page():
    session['corVal'] = 0
    return render_template('login.html')

@router.post('/login')
def login():
    username = request.form['username']
    #query for username in the db
    user = User.query.filter_by(username=username).first()
    #if username is good then go to next step
    if user:
        #If the username is good then we go to the next step in the login process which is image upload for face recognition
        session['username'] = user.username
    else:
        flash("User not found", "error")
        return redirect("/login")
        
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

@router.get('/logout')
def logout():
    # Clear the session data
    session.clear()
    return redirect("/")