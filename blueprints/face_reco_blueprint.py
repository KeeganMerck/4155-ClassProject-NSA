from flask import Blueprint, request, redirect, session, flash, render_template
import os

from modifedFacereco import loginFace
from models.models import db, User

router = Blueprint('facereco', __name__, template_folder='templates')

#For face Reco
#put your face in with the capture and test it with the flask app
#you gotta click caputre, then wait 10 seconds then click upload. Thes ensure taht hte porcessing is complete before
#chcking you, Will be fixed in next ssprint
#You can prolly check with joe but you will need to change the lin 116 to set middle var of the login function to the string of my picture
#Me and crow tapped in like morse code

@router.get('/upload')
def upload_image_page():
    return render_template('camcam.html')

@router.post('/upload')
def upload_image():
    #get the image
    image = request.files['image']
    #if there is an image then 
    if image:
        #save the image
        image.save('uploads/captured-image.png')
        #see if image is loginable
        if loginFace(0, 'uploads/captured-image.png', session['user']) == 1:
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

#CHANGE NAME OF THIS WACK ASS BO
@router.get('/create2')
def uploadTestImages_page():
    return render_template('testPhotos.html')

@router.post('/create2')
def uploadTestImages():
    #on post request:
    session['redire'] = '/create_account'
    
    print(session['currentUser'])
    
    #get the image
    image = request.files['image']
    
    if image:
        #save the image
        paths = "./test/"+str(session['currentUser'])
        pathe = os.path.exists(paths)
        if not pathe:
        # Create a new directory because it does not exist
            os.makedirs(paths)
            print("The new directory is created!")
        image.save(str(paths)+"/"+str(session['currentUser'])+ image.filename)

        flash("Account Created Successfully")
        
    #if there is an image then 
    if("1.png" in image.filename ):
        if loginFace(1, str(paths)+"/"+str(session['currentUser'])+ image.filename, session['currentUser']) == 1:
            return redirect('/login')
    else:
            return redirect('/create_account')
    
    return redirect('/create_account')