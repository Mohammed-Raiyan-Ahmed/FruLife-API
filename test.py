
from flask import Flask, request, jsonify
import os
import numpy as np
from PIL import Image
import tensorflow as tf
from keras_preprocessing.image import load_img, img_to_array
from tensorflow.python.keras.models import load_model
img = load_img("C:\Users\MSA\Desktop\imagepreprocessing\uploads\sign_harish.png", target_size=(300, 300))
x = img_to_array(img)
x = np.expand_dims(img, axis = 0)
res = jsonify(x.tolist())
print(res)
print(type(res))