
from flask import *

from PIL import Image
import requests
import os
from werkzeug.utils import secure_filename
import fnmatch

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from testing import main


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.getcwd() + '/static/img/'
RESULT_FOLDER = os.getcwd() + '/static/img_result/'
RESULT_FOLDER_S = os.getcwd() + '/static/img_result_s/'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['GET', 'POST'])

def predict():
    if len(os.listdir(UPLOAD_FOLDER) ) > 10 :
        [os.remove(UPLOAD_FOLDER+file) for file in os.listdir(UPLOAD_FOLDER) ]
        [os.remove(RESULT_FOLDER+file) for file in os.listdir(RESULT_FOLDER) ]
        [os.remove(RESULT_FOLDER+file) for file in os.listdir(RESULT_FOLDER_S) ]
        
    # take file
    f = request.files["fileUpload"]
    # save file
    filename = secure_filename(f.filename)
  
    f.save(os.path.join(UPLOAD_FOLDER, filename))
    #view
    # img = Image.open(f)
    # print(img.size)
    # plt.imshow(img)
    # plt.show()
    # predict
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    path_result,path_result_s,total_score = main(file_path,filename)

    #myimage = fnmatch.filter(os.listdir(os.path.join(UPLOAD_FOLDER)),)
    
    total_score = total_score.tolist()
    total_score = np.round(total_score[0][0],decimals = 3)
    if total_score >=4.8:
        evaluate = 'Excellent 😍'
    if total_score >= 4:
        evaluate = 'Good Image ❤️'
    elif total_score >=2.5:
        evaluate = 'Not Bad 😘'
    else:
        evaluate = 'Bad Image 😡'
    return render_template('show.html',path = path_result,path_s = path_result_s,score = total_score,evaluate = evaluate)

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0')
