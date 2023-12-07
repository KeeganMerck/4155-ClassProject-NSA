from flask import Blueprint, request, redirect, session, flash, render_template
import os

from modifedFacereco import loginFace
from models.models import db, User
from sesh import checkLoc
router = Blueprint("facereco", __name__, template_folder="templates")

# For face Reco
# put your face in with the capture and test it with the flask app
# you gotta click caputre, then wait 10 seconds then click upload. Thes ensure taht hte porcessing is complete before
# chcking you, Will be fixed in next ssprint
# You can prolly check with joe but you will need to change the lin 116 to set middle var of the login function to the string of my picture
# Me and crow tapped in like morse code


@router.get("/upload")
def upload_image_page():
    print("here")
    #basically, check if the previous page the user was on is correct and then let them through if it is, other than redirec
    if(checkLoc(0) == 1):
        
        return render_template("login_image_cap.html")
    else:
        return redirect("/login", code=302)



@router.route("/upload", methods=["POST", "GET"])
def upload_image():

    
    # on post request:
    if request.method == "POST" and request.files["image"]:
        # get the image
        
        image = request.files["image"]
        # if there is an image then
        if image:
            # save the image
            image.save("uploads/captured-image.png")
            # see if image is loginable
            if loginFace(0, "uploads/captured-image.png", session["username"]) == 1:
                session["corVal"] = 1
                session['page'] = 1 
            else:
                session["corVal"] = 0
            # Save the image to the "uploads" folder
        # if the image iis elog inable then and matches the users face then redirect them to the next pge
        if session.get("corVal") == 1:
            return redirect("/image_grid")
        else:
            # redirect them to the failed page
            flash("Face could not be recognized", "error")
            return redirect("/login")
    #if there is a post request and the face works out then direct to image gird ont he button
    elif request.method == "POST" and session.get("corVal") == 1:
        flash("Face Recognized", "success")
        
        return redirect("/image_grid")
    #if there is a just a post request then make sure they take a picture of their face
    elif request.method == "POST":
        flash("Please complete the 'Capture' feature", "error")

    return render_template("login_image_cap.html")


@router.route("/create2", methods=["POST", "GET"])
def uploadTestImages():
    # on post request:

    if request.method == "POST" and request.files["image"]:
        session["flag"] = 0
        # get the image
        image = request.files["image"]
        if image:
            # save the image
            paths = "static/images/User_Images/" + str(session["currentUser"])
            pathe = os.path.exists(paths)

            if not pathe:
                # Create a new directory because it does not exist
                os.makedirs(paths)
                print("The new directory is created!")

            image.save(str(paths) + "/" + str(session["currentUser"]) + image.filename)

        # if there is an image then
        if "1.png" in image.filename:
            if (loginFace(1, str(paths) + "/" + str(session["currentUser"]) + image.filename, session["currentUser"])== 1):
                session["flag"] = 1
                session.pop("currentUser", None)
                flash("Account Created Successfully", "success")
                return redirect("/login")
        else:
            return redirect("/create_account")

        return redirect("/create2")

    elif request.method == "POST" and session.get("flag") == 1:
        flash("Account Created Successfully", "success")
        return redirect("/login")
        # Save the image to the "uploads" folder
        # if the image is login-able then and matches the users face then redirect them to the next pge
    
    elif request.method == "POST":
        flash("Please complete the 'Capture' feature", "error")

    return render_template("create_account_image_cap.html")
