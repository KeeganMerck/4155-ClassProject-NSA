#Heavily based on website below. Will be changed overtime
#You need c++ installed to make this work aswell
#https://realpython.com/face-recognition-with-python/
#we might have to change a lot still iDk
from pathlib import Path
import pickle
import face_recognition
from collections import Counter
from PIL import Image, ImageDraw 
#important path
DEFAULT_ENCODINGS_PATH = Path("output/encodings.pkl")


Path("output").mkdir(exist_ok=True)

#this guy is a new user being added. 

#folder path names
usertestData = "test"
userValid = "validate"
#Will be deleted when we don't have to draw box over face anymore but good for testing
BOUNDING_BOX_COLOR = "red"
TEXT_COLOR = "white"


#YOU GOTTA ADD TO THE ENCODING FILE IF IT DO NOT EXIST IF IT DO THEN YOU JUST ADD NEW FACE HOW DO I FIGURE OUT WHICH IS NEW?
def encode_known_faces( model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH):
    
    names = []
    encodings = []
    #this path should have the name of the userfolder in it for encoding when a new user is added
    # #change this  
    for filepath in Path(usertestData).glob("*/*"):
        #get the name of teh person from the folder
        name = filepath.parent.name
        #load the image files from that
        image = face_recognition.load_image_file(filepath)
        #find the location
        face_locations = face_recognition.face_locations(image, model=model)
        #get encoding
        face_encodings = face_recognition.face_encodings(image, face_locations)
#append encodings and names to arrays
        for encoding in face_encodings:

            names.append(name)

            encodings.append(encoding)

    name_encodings = {"names": names, "encodings": encodings}
    #dump the encodings in the endcoding file
    with encodings_location.open(mode="wb") as fp:
        pickle.dump(name_encodings, fp)
    
      


def recognize_faces( image_location: str, model: str = "hog",encodings_location: Path = DEFAULT_ENCODINGS_PATH):
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    input_image = face_recognition.load_image_file(image_location)
    #detect input faces in image and then get their encodings which will help identify faces
    input_face_locations = face_recognition.face_locations(   input_image, model=model )
    input_face_encodings = face_recognition.face_encodings( input_image, input_face_locations)

    #get image, draw on image
    pillow_image = Image.fromarray(input_image)

    draw = ImageDraw.Draw(pillow_image)

        #interate through the face locatoins and input face endocings used the zi pfunciton
    #call the recognize face funciton and it doesnt exist here
    for bounding_box, unknown_encoding in zip(input_face_locations, input_face_encodings ):
            name = recognize_face(unknown_encoding, loaded_encodings)
            #if there is no name in the code then you  
            if not name:
                name = "Unknown"
            personName = name
                #bounding box is a variable that shows the face coord
            display_face(draw, bounding_box, name)
            
    #delete the drawing and show the img
    del draw
    pillow_image.show()
    return name
#code after implicity is bolded
def recognize_face(unknown_encoding, loaded_encodings):
    boolean_matches = face_recognition.compare_faces(loaded_encodings["encodings"], unknown_encoding)
    votes = Counter(
        name
        for match, name in zip(boolean_matches, loaded_encodings["names"])
        if match
    )
    if votes:
        return votes.most_common(1)[0][0]

def display_face(draw, bounding_box, name):
    top, right, bottom, left = bounding_box
    draw.rectangle(((left, top), (right, bottom)), outline=BOUNDING_BOX_COLOR)
    text_left, text_top, text_right, text_bottom = draw.textbbox(
        (left, bottom), name
    )
    draw.rectangle(
        ((text_left, text_top), (text_right, text_bottom)),
        fill="blue",
        outline="blue",
    )
    draw.text(
        (text_left, text_top),
        name,
        fill="white",
    )
#add image to validation folder
def validate(model: str = "hog"):

    for filepath in Path(userValid).rglob("*"):

        if filepath.is_file():

            recognize_faces(

                image_location=str(filepath.absolute()), model=model

            )


#called by imcap.py
#all print statements will be deleted once debugging is done
def login(register, login, userName):
#if they are a new account, encode adn validate them, 
    if register == 1:
        encode_known_faces(usertestData)
        validate("hog")
        named = recognize_faces(login, "hog", DEFAULT_ENCODINGS_PATH)
        #if their name does not match the username detected don't let them in 1 and -1 represent in or not
        if named.lower() != userName.lower():
            print("DONT LOG THEM IN NOOOO AHHHHHHH")
            loginVal = -1
        else:
            print("Yeah they're chill")
            loginVal = 1
        print(named, userName)
#if they are not new just get the name detected and then see if they are loginable
    if register == 0:
        named = recognize_faces(login, "hog", DEFAULT_ENCODINGS_PATH)
        print(named, userName)
        if named.lower() != userName.lower():
            print("DONT LOG THEM IN NOOOO AHHHHHHH")
            loginVal = -1
        else:
            print("Yeah they're chill")
            loginVal = 1
    

