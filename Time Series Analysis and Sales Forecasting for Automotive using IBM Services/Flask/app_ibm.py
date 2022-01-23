# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 16:16:19 2022

@author: Hitesh
"""

import joblib
import pandas as pd
from flask import Flask,request,render_template
import os
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "wO8JHOKuRoeaSrIC2KyKeQORrrtlveW1DYS3-eg_31pv"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken} 

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
        print(ds)
        ds['year'] = pd.DatetimeIndex(ds['ds']).year
        ds['month'] = pd.DatetimeIndex(ds['ds']).month
        ds['day'] = pd.DatetimeIndex(ds['ds']).day
        ds.drop('ds', axis=1, inplace=True)
        ds.drop('day', axis=1, inplace=True)
        ds=ds.values.tolist()
        print(ds)
        payload_scoring = {"input_data": [{"fields": [["year", "month"]], "values": ds[0:2]}]}
        response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/dcbf9615-e2dc-4bde-8a1c-e6b2bfeb7ea1/predictions?version=2022-01-22', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        print(response_scoring.json())
        pred=response_scoring.json()
        output= pred['predictions'][0]['values'][0][0]
        
        print(output)
        
        return render_template('predict.html',output='The sale value on selected is Rs. {}'.format(output))
    return render_template("predict.html")


if __name__=="__main__":
    app.run(debug=True)