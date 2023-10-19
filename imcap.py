# program to capture 10 images pythong
from modifedFacereco import login
# importing OpenCV library
#import keyboard button lib
import cv2
import os
import msvcrt
# initialize the camera
register = 0
username = "jerm" 
current_dir = os.getcwd()
final_dr = os.path.join(current_dir, r''"test/"+username)
if not os.path.exists(final_dr):
    os.makedirs(final_dr)
final_v = os.path.join(current_dir, r''"valid/"+username)
if not os.path.exists(final_v):
    os.makedirs(final_v)


if register == 1:
    cam = cv2.VideoCapture(0)
    #loop 10 times
    i = 0
    print("hit da space bar to take pictures ho")
    #if the user hits the spacebar
    if ord(msvcrt.getch()) == 32:
        for i in range(12):
            result, image = cam.read()

            if result and i < 10:

                # showing result, it take frFame name and image
                # output
                cv2.imshow("getFace", image)

                # saving image in local storage
                strang = final_dr+"/"+username+ "Image" + str(i) + ".png"
                print(strang)
                cv2.imwrite(strang, image)

                # If keyboard interrupt occurs, destroy image
                # window
                cv2.waitKey(0)
                cv2.destroyWindow("getFace")

            # If captured image is corrupted, moving to else part
            elif i >=10:
                # showing result, it take frame name and image
                # output
                cv2.imshow("getFace", image)

                # saving image in local storage
                strang = final_v+"/"+username+ "Image" + str(i) + ".png"
                cv2.imwrite(strang, image)

                # If keyboard interrupt occurs, destroy image
                # window
                cv2.waitKey(0)
                cv2.destroyWindow("getFace")
            else:
                print("No image detected. Please! try again")
login(register, "jerb.jpg", username)