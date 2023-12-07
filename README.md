# 4155-ClassProject-NSA
Image-Projection Plus Facial Recognition For User Authentication. Project assigned through NSA and ITIS 4155  

## How to use:  
run `flask run`  
go to `localhost:5000`  
Create an account:  
1 Enter the usual account information: Username, email, and name  
1 Enter extra features such as image category, vertical offset, and horizontal offset values (used when selecting the correct image on the image grid)  
1 Pick a location for images to be projected onto your face and the value of how these images will be rotated (not yet implemented)  
Capture 10 images for account creation:  
1 Select the capture button  
1 Move your face around in a circular motion slowly as the app takes a picture every second, for ten seconds  
1 After receiving a pop-up of an image of you, ensure in the top left corner there is red text stating the `username` you entered in the account creation  
1 You are free to click the upload button  
Login:  
1 Enter a username  
1 Look into the camera and select capture to take a picture for the start of authentication  
1 Allow for an image pop-up to appear with your `username` in red in the top left corner  
1 Wait for a few seconds, then click the upload button  
Image Grid:  
1 Based on the image category you selected in account creation, find the two images that are of that category  
1 After finding two images you must calculate the offset based on the values selected in the account creation  
1 For each image, move to the right the value of the horizontal offset and move down the value of the vertical offset, the image you land on will be the image you select
**If you reach the edge of the grid, continue counting by wrapping back around to the start of either the row or column.  
1 After selecting the TWO images based on the image category and calculating the image offset, click Submit  
You will be sent to the home page and successfully authenticate if you have entered everything correctly.  
