#Heavily based on website below. Changes overtime will come from the exact use we need. This 
#provides a good set of fumnctions for us to get a basic layout
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


#folder path names
usertestData = "static/images/User_Images/"
userValid = "validate"

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
        #find the location of the faces in each image
        face_locations = face_recognition.face_locations(image, model=model)
        #generate encodings
        face_encodings = face_recognition.face_encodings(image, face_locations)
#append encodings and names to arrays
        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

    name_encodings = {"names": names, "encodings": encodings}
    #dump the encodings in the endcoding file
    with encodings_location.open(mode="wb") as fp:
        pickle.dump(name_encodings, fp)
    

def recognize_faces( image_location, model,encodings_location):
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)
    input_image = face_recognition.load_image_file(image_location)
    #detect input faces in image and then get their encodings which will help identify faces
    input_face_locations = face_recognition.face_locations(input_image, model=model)

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
    #compares a face to pictures in folders to see which one matches the most. If tyheres a match theress a vote for taht name
    if votes:
        return votes.most_common(1)[0][0]
#put name in top left corner
def display_face(draw, bounding_box, name):
    
    draw.text((0,0), name, fill="red")

#model is hog which means
def validate(model):
    #go through all of hte folders in the userValidate folder and validate them
    for filepath in Path(userValid).rglob("*"):
        if filepath.is_file():
            recognize_faces(image_location=str(filepath.absolute()), model=model)


#called by imcap.py
#all print statements will be deleted once debugging is done
def loginFace(register, login, userName):
    loginVal = 0
#if they are a new account, encode adn validate them, 
    if register == 1:
        encode_known_faces(usertestData)
        validate("hog")
        named = recognize_faces(login, "hog", DEFAULT_ENCODINGS_PATH)
        #if their name does not match the username detected don't let them in 1 and -1 represent in or not
        if named.lower() != userName.lower():
            print("Failed account creation")
            loginVal = -1
        else:
            print("Successfull account reation")

            loginVal = 1
#if they are not new just get the name detected and then see if they are loginable
    if register == 0:
        #hog is histogram of origneted gradients for object detectiosn and is CPU intensive
        named = recognize_faces(login, "hog", DEFAULT_ENCODINGS_PATH)
        if named.lower() != userName.lower():
            print("Failed login")

            loginVal = -1
        else:
            print("Successfull login")

            loginVal = 1
    
    return loginVal