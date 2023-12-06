from flask import render_template, Blueprint, request, redirect, session, flash
from src.cifar.get_image import single_image
from models.models import db, StackEntry, User
import numpy as np
from PIL import Image
import base64
import io
import random

router = Blueprint("image_selection", __name__, template_folder="templates")


# Image grid form page
@router.get("/image_grid")
def image_page():
    image_nums = []
    img_urls = []
    label_list = [[0 for i in range(5)] for j in range(4)]

    label_count = {
        "0": 0,
        "1": 0,
        "2": 0,
        "3": 0,
        "4": 0,
        "5": 0,
        "6": 0,
        "7": 0,
        "8": 0,
        "9": 0,
    }

    columnCount = 0
    rowCount = 0

    while len(img_urls) < 20:
        # get random number but ensure number is not already in array
        num = random.randrange(0, 5000)
        if not (num in image_nums) and is_unique_within_window(num):
            image_nums.append(num)
        else:
            continue

        # get image and label associated with index
        image, label = single_image(int(num))

        # ensure not more than 2 of each label is in the grid
        label = str(label)[1]
        if label_count[label] == 2:
            continue
        else:
            label_count[label] = label_count[label] + 1

        # push the unique image number to table
        push_to_stack(num)

        # encode image to pass to template
        img = Image.fromarray(np.array(image).astype(np.uint8))
        image_io = io.BytesIO()
        img.save(image_io, "PNG")
        dataurl = "data:image/png;base64," + base64.b64encode(
            image_io.getvalue()
        ).decode("ascii")

        # store dataurls in array
        img_urls.append(dataurl)

        label_list[rowCount][columnCount] = label
        
        columnCount = columnCount + 1
        if(columnCount > 4):
            columnCount = 0
            rowCount = rowCount + 1

    session["label_list"] = label_list

    return render_template("image_grid.html", images=img_urls)


# Processing image grid form selections
@router.post("/process_form.py")
def process_form():
    selected_image1 = request.form.get("selected_image1")
    selected_image2 = request.form.get("selected_image2")

    label_list = session.get("label_list", [])

    print(selected_image1, selected_image2, label_list)

    userObj = User.query.filter_by(username=session["username"]).first()

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

    user_category = label_dict[userObj.imagecategory]

    ##Going to have to add (1 * horizontal)
    ##Going to have to add (5* vertical)
    ##Then have to mod values

    im1_Column = int(selected_image1) // 10
    im1_Row = int(selected_image1) % 10
    im2_Column = int(selected_image2) // 10
    im2_Row = int(selected_image2) % 10

    print(im1_Column, im1_Row, im2_Column, im2_Row)


    if selected_image1 and selected_image2:
        if label_list[im1_Column][im1_Row] == str(user_category) and label_list[im2_Column][im2_Row] == str(user_category):
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
        # Check if the stack has reached its limit (100 entries)
        count = StackEntry.query.count()

        if count >= 400:
            # If there are already 100 entries, remove the oldest entry using FIFO
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
