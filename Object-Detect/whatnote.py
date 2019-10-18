from keras.models import load_model
import cv2
import numpy as np

#reverse class map, if imageset is 0 for PC, then label is shown to user.
REV_CLASS_MAP = {
    0: "50front",
    1: "50back",
    2: "200front",
    3: "200back",
    4: "none"
}

#maps value, which in this case is label
def mapper(val):
    return REV_CLASS_MAP[val]

#if iteration for displaying labels
def currency_names(currency_name):
    if currency_name == "50front":
        return "Rs. 50 Front Side"

    if currency_name == "50back":
        return "Rs.50 Back Side"

    if currency_name == "none":
        return "Waiting"

    if currency_name == "200front":
        return "Rs. 200 Front Side"

    if currency_name == "200back":
        return "Rs. 200 Back Side"


#previously trained model
model = load_model("notes-model.h5")

#access camera
cap = cv2.VideoCapture(0)

#presume nothing is seen as of opening camera,
#hence it runs a loop of keeping camera open
note_seen = None

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # rectangle for user
    cv2.rectangle(frame, (100, 100), (300, 300), (255, 255, 255), 2)
    # rectangle for computer to show its output
    cv2.rectangle(frame, (200, 200), (600, 200), (255, 255, 255), 2)

    # extract the region of image within the user rectangle
    roi = frame[100:300, 100:300]
    img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (220, 220))

    # predict the note seen by camera
    pred = model.predict(np.array([img]))
    currency_code = np.argmax(pred[0])
    currency_name = mapper(currency_code)

    # show computer prediction, notes and none
    if note_seen != currency_name:
        if currency_name != "none":
            currency_name = currency_names(currency_name)
    else:
        currency_name = "none"


    # display text
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "Show Notes",
                (50, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Note predicted is " + currency_name,
                (50, 100), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow("Currency Note Predictor", frame)

#button 'q' to close camera and stop all windows.
    k = cv2.waitKey(10)
    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
