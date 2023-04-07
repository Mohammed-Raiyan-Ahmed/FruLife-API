# FruLife API

FruLife is a Flask based API service, which serves a deep learning model.
The deep learning model is used to predict the shelf life of a fruit. Currently only
one model (for predicting the shelf life of banana) is deployed via this API.

Requirements:
Run the following commands in your working directory:

1. pip install flask numpy Pillow keras_preprocessing keras
2. pip install tensorflow
3. mkdir uploads
Note the Lort at which the API server is running... Mostly runs on
http://127.0.0.1:5000/upload

The api should contain a form data with field key "photo", whose value should be an image file.

The extensions of the image file could be {png, jpg, jpeg}
