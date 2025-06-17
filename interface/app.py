from flask import Flask , render_template , url_for , request
from flask import redirect , session

import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from PIL import Image
import shutil
import datetime
import os


def clear():
    files = os.listdir("upload")
    for i in files:
        os.unlink(os.path.join("upload", i))
#get date as string to rename files
def getDate():
    dt = datetime.datetime.now()
    dt = str(dt)
    dtt = dt.replace(" ","")
    dt = dtt.replace(".","_")
    dtt = dt.replace(":","_")
    dt = dtt.replace("-","_")
    return dt
#get file extention
def extOf(file):
    ext = os.path.splitext(file)[1]
    return ext

target = [  'Fresh Apple',
            'Fresh Apricot',
            'Fresh Avocado',
            'Fresh Banana',
            'Fresh Cherry',
            'Fresh Date',
            'Fresh Grape',
            'Fresh Lemon',
            'Fresh Mango',
            'Fresh Orange',
            'Fresh Tomato',
            'Fresh Watermelon',
            'Not Fruit',
            'Rotten Apple',
            'Rotten Apricot',
            'Rotten Avocado',
            'Rotten Banana',
            'Rotten Cherry',
            'Rotten Date',
            'Rotten Grape',
            'Rotten Lemon',
            'Rotten Mango',
            'Rotten Orange',
            'Rotten Tomato',
            'Rotten Watermelon'
            ]
maxPred = 0

app = Flask(__name__)
app.secret_key = "super secret key"

model = load_model("models/model_final100.h5")

@app.route('/')
def index():
    
    return render_template("index.html")

@app.route("/upload-target" , methods = ['POST'])
def upload():
    #delete older file
    clear()
    file = request.files['file']
    fname = file.filename
    file.save(os.path.join("upload",fname))

    new_name = getDate() + extOf(fname)

    os.rename(os.path.join("upload",fname) ,os.path.join("upload",new_name))
    fname = new_name
    session["fname"] = fname
    if os.path.exists("static/detect.txt"):
        os.unlink("static/detect.txt")
    return redirect("/detect")

@app.route("/add")
def add():
    if not os.path.exists(os.path.join("data", session["class"])):
        os.makedirs(os.path.join("data", session["class"]))
    
    dest = os.path.join("data", session["class"])
    destination = os.path.join(dest, session["fname"])
    source = os.path.join("upload",session["fname"])
    shutil.move(source, destination)
    
    return '', 204

@app.route("/detect")
def detect():
    
    imgname = session["fname"]
    uploaded_image = os.path.join("upload",imgname)
    img = image.load_img(uploaded_image, color_mode="rgb", target_size=(150, 150), interpolation="nearest")
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = img/255
    images = np.vstack([img])
    classes = model.predict(images, batch_size=10)
    valS = (-classes[0]).argsort()[:5]
    result_file = open("static/detect.txt", "w")
    result_file.close()
    result_file = open("static/detect.txt", "a")
    
    session["maxPred"] = classes[0][0] * 100
    session["class"] = target[valS[0]]
    for i in valS:
        l = target[i]
        percent = classes[0][i] * 100
        p = str(percent)
        x =  '{ "prediction":"'+l+'" , "precision" : "'+p+'"}'
        result_file.write(x)
    result_file.close()

    return '', 204

if __name__ == "__main__":
    app.run(debug = True,port=80)
