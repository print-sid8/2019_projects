## CUSTOM OBJECT DETECTION USING OPENCV, KERAS, AND DEEP LEARNING(SQUEEZENET)

Hi,

The entire detailed step by step procedure is attached in the Docs pdf file.

Pre-requisites to install are in the requirements.txt file.

Please use Python Virtual Environment, so that there are minimal errors.

Install the requirements.txt file using this command below, in your cmd, which is inside the virtual environment -
pip install -r requirements.txt 

Then follow the instructions

Methodology –

1)	Image Dataset collection                   - with gatherimage.py
2)	Selecting/Designing a Neural Net           - I used Keras sequential model with SqueezeNet as first layer, and rELU and softmax as next 2. 
3)	Train the Model                            - with trainn.py
4)	Test the Model                             - with testt.py and random images from gathered data set
5)	Deploy Model in Computer                   - whatnote.py , since I was training it on currency notes.

If you want convert the final model to a mobile level model, then use the "googlecolab.ipynb" file to do so, it converts Keras Model to TFLite using Google Colab.
