from flask import Flask, render_template, request
import pickle 
import matplotlib.pyplot as plt
import cv2
import numpy as np
import tensorflow as tf
import os
# from tensorflow.keras.preprocessing.image import load_img

type(5)
with open("final.pkl", "rb") as file:
    model = pickle.load(file)

# Create Server
app = Flask(__name__, static_folder='static')

# Configuration settings for image upload
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if the uploaded file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    # Check whether images is present in the list of request-able files
    if 'image' not in request.files:
        # return 'No image part'
        return render_template('index.html', output='No image part')

    # Handle the image upload
    uploaded_file = request.files['image']
    if uploaded_file.filename == '':
        # return 'No selected file'
        return render_template('index.html', output='No selected file')

    if uploaded_file and allowed_file(uploaded_file.filename):  # Check if the uploaded file has an allowed extension
        filename = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(filename)  # Save the uploaded file

        img = tf.keras.preprocessing.image.load_img(filename, target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img)
        print(type(img_array))
        img_array = np.array([img_array])
        print(type(img_array))
        print(img_array.shape)
        predictions = model.predict(img_array)
        print(predictions)
        class_id = np.argmax(predictions, axis=1)
        print(class_id)
        class_names = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']
        result = class_names[class_id.item()]

        return render_template('index.html', output=str.capitalize(result))
    return 'File format not allowed'


# start the server
app.run(host="0.0.0.0")
