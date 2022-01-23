# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 14:09:59 2022

@author: Hitesh
"""

import joblib
import pandas as pd
from flask import Flask,request,render_template
import os
from gevent.pywsgi import WSGIServer 

app=Flask(__name__)
model=joblib.load('sales.sav')

@app.route('/')
def home():
    return render_template('predict.html')

@app.route('/predict',methods=['POST'])
def y_predict():
    if request.method=="POST":
        ds=request.form['date']
        a={'ds':[ds]}
        ds=pd.DataFrame(a)
        prediction=model.predict(ds)
        print(prediction)
        output=round(prediction.iloc[0,15],1)
        return render_template('predict.html',output='The sale value on selected is Rs. {}'.format(output))
    return render_template("predict.html")

port=os.getenv('VCAP_APP_PORT','8080')
if __name__=="__main__":
    app.secret_key= os.urandom(12)
    app.run(debug=True,host='0.0.0.0',port=port)