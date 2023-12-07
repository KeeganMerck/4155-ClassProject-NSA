from flask import render_template, Blueprint, request, redirect, session, flash
from src.cifar.get_image import single_image
from models.models import db, StackEntry, User
import numpy as np
from PIL import Image
import base64
import io
import random
from sesh import checkLoc
router = Blueprint("image_selection", __name__, template_folder="templates")


# Image grid form page
@router.get("/image_grid")

def image_page():
    image_nums = []
    img_urls = []
    label_list = [[0 for i in range(5)] for j in range(4)]

    # Count occurrences of each label to ensure no more than 2 of each in the grid
    label_count = {
        "0": 0, "1": 0, "2": 0, "3": 0, "4": 0,
        "5": 0, "6": 0, "7": 0, "8": 0, "9": 0,
    }

    yCount = 0
    xCount = 0

    # Loop until 20 unique images are collected
    while len(img_urls) < 20:
        # Get a random number, ensuring it's not already in the array
        num = random.randrange(0, 5000)
        if not (num in image_nums) and is_unique_within_window(num):
            image_nums.append(num)
        else:
            continue

        # Get image and label associated with index
        image, label = single_image(int(num))

        # Ensure not more than 2 of each label is in the grid
        label = str(label)[1]
        if label_count[label] == 2:
            continue
        else:
            label_count[label] += 1

        # Push the unique image number to table
        push_to_stack(num)

        # Encode image to pass to template
        img = Image.fromarray(np.array(image).astype(np.uint8))
        image_io = io.BytesIO()
        img.save(image_io, "PNG")
        dataurl = "data:image/png;base64," + base64.b64encode(
            image_io.getvalue()
        ).decode("ascii")

        # Store dataurls in array
        img_urls.append(dataurl)

        # Update label_list with the current label
        label_list[xCount][yCount] = int(label)
        
        yCount += 1
        if(yCount > 4):
            yCount = 0
            xCount += 1

    # Store the label_list in the session for later use
    session["label_list"] = label_list
    if(checkLoc(1) == 1):
        session['page'] = 1  
        return render_template("image_grid.html", images=img_urls)
    else:
        return redirect("/login", code=302)
    


# Processing image grid form selections
@router.post("/process_form.py")
def process_form():

    # Retrieve selected image IDs from the form
    selected_image1 = request.form.get("selected_image1")
    selected_image2 = request.form.get("selected_image2")

    # Retrieve label list from the session
    label_list = session.get("label_list", [])

    # Retrieve user object from the database
    userObj = User.query.filter_by(username=session["username"]).first()

    # Mapping of image categories to corresponding numerical values
    label_dict = {
        "Planes": 0,
        "Cars": 1,
        "Birds": 2,
        "Cats": 3,
        "Deers": 4,
        "Dogs": 5,
        "Frogs": 6,
        "Horses": 7,
        "Boats": 8,
        "Trucks": 9,
    }
    
    # Get the numerical value of the user's image category
    user_category = label_dict[userObj.imagecategory]

    if selected_image1 and selected_image2:
        # Extract row and column indices from the selected image IDs
        im1_x = int(selected_image1) % 10
        im1_y = int(selected_image1) // 10
        im2_x = int(selected_image2) % 10
        im2_y = int(selected_image2) // 10

        imgs_user_cat = []

        # Iterate through the label_list to find images with the user's category
        for y in range(len(label_list)):
            for x in range(len(label_list[y])):
                if label_list[y][x] == user_category:
                    imgs_user_cat.append((x, y))

        # Calculate images users should have selected based off of category and offset
        # Modulo used to "wrap around" the image grid
        correct_x1 = (imgs_user_cat[0][0] + userObj.horizontal) % (len(label_list[0]))
        correct_y1 = (imgs_user_cat[0][1] + userObj.vertical) % (len(label_list))
        correct_x2 = (imgs_user_cat[1][0] + userObj.horizontal) % (len(label_list[0]))
        correct_y2 = (imgs_user_cat[1][1] + userObj.vertical) % (len(label_list))
        
        # Authenticate based on the selected images and their positions
        if (
            # Check if either of the selected images matches the first correct position
            (im1_x == correct_x1 and im1_y == correct_y1) or
            (im1_x == correct_x2 and im1_y == correct_y2)
        ) and (
            # Check if either of the selected images matches the second correct position
            (im2_x == correct_x1 and im2_y == correct_y1) or
            (im2_x == correct_x2 and im2_y == correct_y2)
        ):
            flash("Authentication Succesfull", "success")
            return redirect("/home_page")
        else:
            flash("Incorrect images selected", "error")
            return redirect("/image_grid")

    else:
        flash("Please select two images before submitting", "error")
        return redirect("/image_grid")


def push_to_stack(data):
    # Check if the data is unique within the specified window
    if is_unique_within_window(data):
        # Check if the stack has reached its limit (400 entries)
        count = StackEntry.query.count()

        if count >= 400:
            # If there are already 400 entries, remove the oldest entry using FIFO
            oldest_entry = StackEntry.query.order_by(StackEntry.timestamp).first()
            db.session.delete(oldest_entry)

        # Insert the new number into the stack with the current timestamp
        new_entry = StackEntry(data=data)
        db.session.add(new_entry)
        db.session.commit()


def is_unique_within_window(data, window_size=400):
    recent_entries = (
        StackEntry.query.order_by(StackEntry.timestamp.desc()).limit(window_size).all()
    )
    recent_numbers = [entry.data for entry in recent_entries]
    return data not in recent_numbers
