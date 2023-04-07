from flask import Flask, request, jsonify
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from keras_preprocessing.image import load_img, img_to_array
from tensorflow.python.keras.models import load_model

app = Flask(__name__)

predict_model_path = 'banana_custom_model.h5' #Enter the path of the shelf-life model
predict_model = load_model(predict_model_path, compile = False)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'photo' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    photo = request.files['photo']

    # if user does not select file, browser also
    # submit an empty part without filename
    if photo.filename == '':
        return jsonify({'message': 'No file selected for uploading'}), 400

    if photo and allowed_file(photo.filename):
        filename = photo.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(filepath)
        x = str(preprocess(filepath))
        os.remove(filepath)
        return x
    else:
        return jsonify({'message': 'Invalid file type, only PNG, JPG, JPEG, and GIF images are allowed'}), 400

def preprocess(img_path):
    labels_predict = {0: '3 - 4 ', 1: '5 - 8 ', 2: '1 ', 3: '2 - 3 ', 4: '0 ', 5: '6 - 7 '}
    days_shelf = ['3 - 4 ','6 - 7 ', '1' , '2 - 3 ' , '0','5 - 6']
    img = Image.open(img_path)
    img = img.resize((256, 256))
    
    # Convert PIL image to numpy array
    img_array = img_to_array(img)
    
    # Normalize pixel values
    img = np.expand_dims(img, axis=0)
    img = img / 255.0

    # make predictions
    prediction = predict_model.predict(img)
    predicted_class = np.argmax(prediction)
    predicted_label = days_shelf[predicted_class]
    return predicted_label

if __name__ == '__main__':
    app.run(debug=True)
