desc = '''Script to gather data images with a particular label.

Usage: python gather_images.py <label_name> <num_samples>

The script will collect <num_samples> number of images and store them
in its own directory.

Only the portion of the image within the box displayed
will be captured and stored.

Press 'a' to start/pause the image collecting process.
Press 'q' to quit.

'''

import cv2
import os
import sys

#try looks for errors and sends to except if the argument provided is mising

try:
    label_name = sys.argv[1]
    num_samples = int(sys.argv[2])
except:
    print("Arguments missing.")
    print(desc)
    exit(-1)

# defining save folder, and individual folders will be made in it for each object.

IMG_SAVE_PATH = 'image_data'
IMG_CLASS_PATH = os.path.join(IMG_SAVE_PATH, label_name)

# makes directory for each object class
# then collects all images of that class in that folder
try:
    os.mkdir(IMG_SAVE_PATH)
except FileExistsError:
    pass
try:
    os.mkdir(IMG_CLASS_PATH)
except FileExistsError:
    print("{} directory already exists.".format(IMG_CLASS_PATH))
    print("All images gathered will be saved along with existing items in this folder")

#opens in built camera, not external camera
    
cap = cv2.VideoCapture(0)

start = False
count = 0

#keeps camera open in a loop

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    if count == num_samples:
        break
    
#rectangle for user, to show the object to be trained
    
    cv2.rectangle(frame, (80, 80), (300, 300), (255, 255, 255), 2)

#takes pictures from camera till specified number in cmd line
# pictures will be labelled in increasing numbers
# and will be saved to path provided, by creating folder in provided class name
    
    if start:
        roi = frame[80:300, 80:300]
        save_path = os.path.join(IMG_CLASS_PATH, '{}.jpg'.format(count + 1))
        cv2.imwrite(save_path, roi)
        count += 1
    
#texts to be shown while camera is open
        
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Collecting {}".format(count),
            (5, 50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Collecting images", frame)
    
# ordering camera to start clicking with key 'a'
# and then key 'q' to close camera and all windows

    k = cv2.waitKey(10)
    if k == ord('a'):
        start = not start

    if k == ord('q'):
        break
    

print("\n{} image(s) saved to {}".format(count, IMG_CLASS_PATH))
cap.release()
cv2.destroyAllWindows()
