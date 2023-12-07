# 4155-ClassProject-NSA
Image-Projection Plus Facial Recognition For User Authentication. Project assigned through NSA and ITIS 4155

## How to use:
run `flask run`
go to `localhost:5000`
Create an account:
  Enter the usual account information: Username, email, and name
  Enter extra features such as image category, vertical offset, and horizontal offset values (used when selecting the correct image on the image grid)
  Pick a location for images to be projected onto your face and the value of how these images will be rotated (not yet implemented)
Capture 10 images for account creation:
  Select capture button
  Move your face around in a circular motion slowly as the app takes a picture every second, for ten seconds
  After receiving a pop-up of an image of you, ensure in the top left corner there is red text stating the `username` you entered in the account creation
  You are free to click the upload button
Login:
  Enter a username
  Look into the camera and select capture to take a picture for the start of authentication
  Allow for an image pop-up to appear with your `username` in red in the top left corner
  Wait for a few seconds, then click the upload button
Image Grid:
  Based on the image category you selected in account creation, find the two images that are of that category
  After finding two images you must calculate the offset based on the values selected in the account creation
  For each image, move to the right the value of the horizontal offset and move down the value of the vertical offset, the image you land on will be the image you select
    **If you reach the edge of the grid, continue counting by wrapping back around to the start of either the row or column.
  After selecting the TWO images based on the image category and calculating the image offset, click Submit
You will be sent to the home page and successfully authenticate if you have entered everything correctly.
