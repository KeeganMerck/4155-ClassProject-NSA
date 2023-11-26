from flask import render_template, Blueprint, request, redirect, session, flash
from src.cifar.get_image import single_image
from models.models import db, StackEntry
import numpy as np
from PIL import Image
import base64
import io
import random

user_category = 0 #correct category is 0 (planes)

router = Blueprint('image_selection', __name__, template_folder='templates')

#Image grid form page
@router.get('/image_grid')
def image_page():
    image_nums = []
    img_urls = []
    label_list = []

    label_count = {"0":0, "1":0, "2":0, "3":0, "4":0, "5":0, "6":0, "7":0, "8":0, "9":0}

    while len(img_urls) < 20:
        # get random number but ensure number is not already in array
        num = random.randrange(0,5000)
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

        #encode image to pass to template
        img = Image.fromarray(np.array(image).astype(np.uint8))
        image_io = io.BytesIO()
        img.save(image_io, 'PNG')
        dataurl = 'data:image/png;base64,' + base64.b64encode(image_io.getvalue()).decode('ascii')

        #store dataurls in array
        img_urls.append(dataurl)
        label_list.append(label)

    session['label_list'] = label_list

    return render_template('image_grid.html', images = img_urls)

#Processing image grid form selections
@router.post('/process_form.py')
def process_form():
    selected_image1 = request.form.get('selected_image1')
    selected_image2 = request.form.get('selected_image2')

    label_list = session.get('label_list', [])
    
    if selected_image1 and selected_image2:

        #Display label numbers of selected images
        #print(label_list[int(selected_image1)], label_list[int(selected_image2)])
    
        if(label_list[int(selected_image1)] == str(user_category) and label_list[int(selected_image2)] == str(user_category)):
            flash("Authentication Succesfull", "success")
            return redirect("/home_page")
        else:
            flash("Incorrect images selected", "error")
            return redirect("/")

    else:
        flash("Please select two images before submitting", "error")
        return redirect("/")

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
    recent_entries = StackEntry.query.order_by(StackEntry.timestamp.desc()).limit(window_size).all()
    recent_numbers = [entry.data for entry in recent_entries]
    return data not in recent_numbers
