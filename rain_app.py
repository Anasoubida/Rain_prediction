# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 21:30:36 2023

@author: Anas
"""

from fastapi import FastAPI, Query, UploadFile, File
import pickle
from pydantic import BaseModel, Field
import numpy as np
from typing import List
import pandas as pd
from io import BytesIO
import uvicorn


# loading the model and the data transformer
pickle_in = open("model.bin","rb")
classifier=pickle.load(pickle_in)

pickle_in = open("dv.bin","rb")
dv=pickle.load(pickle_in) 
features=dv.get_feature_names_out()
# feature_fr=['Température de rosée','Humidité','Mois','Pression','Température','La vitesse du vent']
# val_pred=[[5,18,2,1015,25,32]]

def predict(data):
    y_pred=classifier.predict(data)[0]
    y_pred_prob=classifier.predict_proba(data)[0][1]
    return {"FR : La prévision qu'il y aura des précipitation est : {}, la probabilité qu'il y aura des précipitations est de {}".format(y_pred,y_pred_prob),
            "EN : The forecast that it will rain is: {}, the probability that it will rain is {}".format(y_pred,y_pred_prob)}
    
# predict(val_pred)



class Input(BaseModel):
    dewptm: float = Field(description="Dew point", gt=0)
    hum: float = Field(description="Humidity", gt=0)
    month: float = Field(description="Month", gt=0)
    pressurem: float = Field(description="Pressure", gt=0)
    tempm: float = Field(description="Temperature", gt=0)
    wspdm: float = Field(description="Wind speed", gt=0)

class Data(BaseModel):
    file: UploadFile
    required_columns: List[str] = list(features)


## API
app=FastAPI()
@app.get('/')
def hello():
    return "Hello, this is an API to predict if it will rain or not in New Delhi"


@app.post('/predict')  
def predict_rain(
        dewptm: float = Query(...,description="Dew point (Température de rosée)",gt=0, lt=60),
        hum: float = Query(...,description="Humidity (Humidité)",gt=0, lt=100),
        month: float = Query(...,description="Month (Mois)",gt=0, le=12),
        pressurem: float = Query(...,description="Pressure (Pression)",gt=0, lt=1086),
        tempm: float = Query(...,description="Temperature (Température)",gt=0, lt=60),
        wspdm: float = Query(...,description="Wind speed (La vitesse du vent)",gt=0, lt=240),
        
        ):
    data = np.array([[dewptm,hum,month,pressurem,tempm,wspdm]])

    return predict(data)    

# try this , and search how to download the result
@app.post('/predict_from_file')  
def predict_rain_file(data: UploadFile = File(...)):
    # df = pd.read_csv(data.filename)
    contents = data.file.read()
    buffer = BytesIO(contents)
    df = pd.read_csv(buffer,sep=';')
    buffer.close()
    data.file.close()
    # df = pd.read_csv("data/test_api.csv",sep=';')
    df.dropna(inplace=True)
    missing_columns = set(features) - set(df.columns)
    if missing_columns:
        return {"error": f"The following columns are missing: {missing_columns}"}
    print(df)
    df_test=dv.transform(df[features].to_dict(orient='records'))
    print(df_test)
    df['rain_pred']=classifier.predict(df_test)
    df['rain_pred_proba']=classifier.predict_proba(df_test)[:,1]
    
    # res = df.to_json(orient="records")
    # parsed = json.loads(res)
    return df.to_dict(orient='records')

@app.post('/predict_body')
def predict_rain_body(data:Input):
    data = data.dict()
    dewptm=data["dewptm"]
    hum=data['hum']
    month=data["month"]
    pressurem=data["pressurem"]
    tempm=data["tempm"]
    wspdm=data["wspdm"]


    data = np.array([[dewptm,hum,month,pressurem,tempm,wspdm]])
    print(dewptm)
    print(type(dewptm))
    print(data)
    # predict(data)
    return predict(data)
 

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)




# dewptm=20&hum=2&month=2&pressurem=500&tempm=20&wspdm=50


