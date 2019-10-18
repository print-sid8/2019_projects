import cv2
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.layers import Activation, Dropout, Convolution2D, GlobalAveragePooling2D
from keras.models import Sequential
import tensorflow as tf
import os

#directory to stored images

IMG_SAVE_PATH = 'image_data'

#giving classes thier numbers for neural net to understand

CLASS_MAP = {
    "50front": 0,
    "50back": 1,
    "200front": 2,
    "200back": 3,
    "none": 4
}

#number of classes using len, to define number of neurons

NUM_CLASSES = len(CLASS_MAP)

#mapper takes value from class map above
def mapper(val):
    return CLASS_MAP[val]

#adding squeenet neural net , sequential model due to keras
'''

-first layer of squeenet is a sequential model.
-second layer is a dropout of 50%, to avoid overfitting.
-third line is the end of SqueezeNet,then we activate rELU(rectified linear unit).
-finally, global average pooling gets average output of each feature map from
 rELU, hence reduces data and gets ready to classify by softmax.
-softmax gives probabilty of each layer, anywhere from 0 to 1,
 hence, sum of all vectors will be 1 at the end.

'''

def get_model():
    model = Sequential([
        SqueezeNet(input_shape=(220, 220, 3), include_top=False),
        Dropout(0.5),
        Convolution2D(NUM_CLASSES, (1, 1), padding='valid'),
        Activation('relu'),
        GlobalAveragePooling2D(),
        Activation('softmax')
    ])
    return model


# load images from the directory, it iterates over every image

dataset = []
for directory in os.listdir(IMG_SAVE_PATH):
    path = os.path.join(IMG_SAVE_PATH, directory)
    if not os.path.isdir(path):
        continue
    for item in os.listdir(path):
        
        # to make sure no hidden files get in our way
        
        if item.startswith("."):
            continue
        
            #load images into memory
        
        img = cv2.imread(os.path.join(path, item))
        
        #convert images into RGB from BGR, occured due to OpenCV
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        #resize or confirming size bcoz squeezenet has been defined earlier
        
        img = cv2.resize(img, (220, 220))

        #directory name is appended, which is written as currency note value by user,
        # which the neural net thinks is a label
        
        dataset.append([img, directory])

'''
DATASET looks like this -
array of image data and corresponding labels
dataset = [
    [[...], '50front'],
    [[...], '200back'],
    ...
]
'''

#unpack image data and labels into respective lists, using mapper defined above

data, labels = zip(*dataset)
labels = list(map(mapper, labels))


'''
lists would look like this -

labels: fifty,twohund,twohundfr,fiftyb,...
one hot encoded: [1,0,0], [0,1,0], [0,1,0], [0,0,1],...
'''

# one hot encode the labels, automatically categorize
# 'labels' as integers for KERAS

labels = np_utils.to_categorical(labels)

# calling the model to train

model = get_model()
model.compile(
    
#adam optimizer to optimize accuracy and learning rates
    
    optimizer=Adam(lr=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# start training, by passing in image data list , and label list,
# with n number of iterations

model.fit(np.array(data), np.array(labels), epochs=7)

# save the model for later use

model.save("notes-model.h5")
