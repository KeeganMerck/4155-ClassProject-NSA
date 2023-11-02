from flask import render_template, Blueprint, request, redirect, session, flash
from src.cifar.get_image import single_image
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
        #get random number but ensure number is not already in array
        num = random.randrange(0,5000)
        if(not (num in image_nums)):
            image_nums.append(num)
        else:
            continue

        #get image and label associated with index
        image, label = (single_image(int(num))) 

        #esnure not more than 2 of each label is in grid
        label = str(label)[1]
        if(label_count[label] == 2):
            continue
        else:
            label_count[label] = label_count[label] + 1

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

#Authentication successful page
@router.get('/home_page')
def success():
    return render_template('home_page.html')