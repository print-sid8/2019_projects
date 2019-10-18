from keras.models import load_model
import cv2
import numpy as np
import sys

#it will take the argument, or path given into cmd line as filepath
filepath = sys.argv[1]

#if model predicts any imaedata, the output will be labels.
REV_CLASS_MAP = {
    0: "twohundfr",
    1: "twohund",
    2: "fifty",
    3: "fifty",
    4: "fiftyb",
    5: "none"
}

#maps value, which in this case is label
def mapper(val):
    return REV_CLASS_MAP[val]


model = load_model("currencynote-model.h5")

# prepare the image from cmd line

img = cv2.imread(filepath)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (220, 220))

# predict the currency note

pred = model.predict(np.array([img]))

#'argmax' looks for index of the array predicted,
# that is, by looking for the largest value in array.

currency_code = np.argmax(pred[0])

# it then takes that index, and maps it with the mapper defined above,
# to get the human readable name.

currency_name = mapper(currency_code)

print("Predicted: {}".format(currency_name))
