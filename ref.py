from flask import Flask, request, jsonify
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from keras_preprocessing.image import load_img, img_to_array
from tensorflow.python.keras.models import load_model
import keras

app = Flask(__name__)


gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  # Restrict TensorFlow to only use the first GPU
  try:
    tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
  except RuntimeError as e:
    # Visible devices must be set at program startup
    print(e)
predict_model_path = 'models/banana_predict_shelf_v2.h5' #Enter the path of the shelf-life model
predict_model = load_model(predict_model_path, compile = False)
@app.route('/upload', methods=['POST'])
def upload_file():
    # retrieve uploaded file from request
    file = request.files['file']
    
    # create directory if it does not exist
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
        
    # save file to the 'uploads' directory
    filename = file.filename
    file.save(os.path.join('uploads', filename))
    file_path = './uploads/'+filename
    x = str(preprocess(file_path))
    return x

def preprocess(img_path):
    labels_predict = {0: '3 - 4 days', 1: '5 - 8 days', 2: '1 day', 3: '2 - 3 days', 4: '0 days', 5: '6 - 7 days'}
    img = load_img(img_path, target_size=(300, 300))
    x = img_to_array(img)
    x = np.expand_dims(img, axis = 0)
    answer = predict_model.predict(x)
    y_class = answer.argmax(axis=-1)
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels_predict[y]
    print(res)
    return res.capitalize(), y_class

if __name__ == '__main__':
    app.run(debug=True)