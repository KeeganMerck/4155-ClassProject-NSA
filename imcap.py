#
#
#  _____ _   _  _____ _______ _____  _    _  _____ _______ _____ ____  _   _  _____
# |_   _| \ | |/ ____|__   __|  __ \| |  | |/ ____|__   __|_   _/ __ \| \ | |/ ____|
#   | | |  \| | (___    | |  | |__) | |  | | |       | |    | || |  | |  \| | (___
#   | | | . ` |\___ \   | |  |  _  /| |  | | |       | |    | || |  | | . ` |\___ \
# # _| |_| |\  |____) |  | |  | | \ \| |__| | |____   | |   _| || |__| | |\  |____) |
# |_____|_| \_|_____/   |_|  |_|  \_\\____/ \_____|  |_|  |_____\____/|_| \_|_____/
# ----------------------------------------------------------------------------------
# Try doing pip install -r requirements.txt
# if it tells you to install the C++  do that through the corrrect link
# ONce all the dependencies are installed, run python imcap.py in the bash terminal
# --OPTIONS---
# register = 0 when using an existing username and account = 1 with a new one
# username = username who is logging in with the picture
# loginimage = the imagethat will be verified with the face recognition system
# ***when this is incorporated with the resto f the applications these will be taken from the app so this file will not have to be
# user edited


from modifedFacereco import loginFace

# importing OpenCV library
# import keyboard button lib
import cv2
import os
import msvcrt

# initialize the cameraera
register = 0
loginimage = "kmercktest.png"
# this var will be changed for when we start getting a usernaem from the website
username = "kmerck"
current_dir = os.getcwd()

# directory informatoin about stuff
final_dr = os.path.join(current_dir, r"" "static/images/User_Images/" + username)
if not os.path.exists(final_dr):
    os.makedirs(final_dr)
final_v = os.path.join(current_dir, r"" "valid/" + username)
if not os.path.exists(final_v):
    os.makedirs(final_v)


if register == 1:
    camera = cv2.VideoCapture(0)
    # loop 10 times
    i = 0
    print(
        "Hit the space bar 10 time while you rotate your face clockwise to take photos of yourself at different angles"
    )
    # if the user hits the spacebar
    if ord(msvcrt.getch()) == 32:
        for i in range(12):
            result, image = camera.read()

            if result and i < 10:
                cv2.imshow("getFace", image)

                # save the image intro the correct place
                strang = final_dr + "/" + username + "Image" + str(i) + ".png"
                cv2.imwrite(strang, image)

                # wait for hte next key press and delete the current up window
                cv2.waitKey(0)
                # cv2.destroyWindow("getFace")

            # If captured image is corrupted, moving to else part
            elif i >= 10:
                cv2.imshow("getFace", image)
                # save image to validation folder
                strang = final_v + "/" + username + "Image" + str(i) + ".png"
                cv2.imwrite(strang, image)

                cv2.waitKey(0)
                cv2.destroyWindow("getFace")
            else:
                print("No image detected. Please! try again")
# jerb.jpg will be changed out for the user captured image from their facecamera when they recognize themselves in
loginFace(register, loginimage, username)
