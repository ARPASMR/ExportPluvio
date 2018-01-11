#inizializzazione
import os
#import pandas as pd
#import numpy as np
#from pandas import Series, DataFrame, Panel
from sqlalchemy import *
import datetime as dt
import json as js
import requests
datafine=dt.datetime.now()
datainizio=datafine-dt.timedelta(hours=1)
Query="Select IDsensore,DataFine,DataInizio,AggregazioneTemporale from A_Sensori join A_Stazioni on A_Sensori.IDstazione=A_Stazioni.IDstazione where IDrete in (1,2,4) and NOMEtipologia = 'PP' and DataFine is NULL;"
engine = create_engine('mysql+mysqlconnector://guardone:guardone@10.10.0.6/METEO')
conn=engine.connect()
df_sensori=pd.read_sql(Query, conn)


frame_dati={}
frame_dati["sensor_id"]=0
frame_dati["function_id"]=3
frame_dati["operator_id"]=4
frame_dati["granularity"]=1
frame_dati["start"]=datainizio.strftime("%Y-%m-%d %H:%M")
frame_dati["finish"]=datafine.strftime("%Y-%m-%d %H:%M")
for f in df_sensori.IDsensore:
    cum=0
    frame_dati["sensor_id"]=f
    richiesta={
    'header':{'id': 10},
    'data':{'sensors_list':[frame_dati]}
    }
    r=requests.post(url,data=js.dumps(richiesta),headers=headers)
    
    if(js.loads(r.text)['data']['outcome']==0):
        a=js.loads(r.text)['data']['sensor_data_list'][0]['data']
        for row in range(1,len(a)-2):
            riga=a[row]
            h=int(riga['datarow'].split(";")[2])
            if (h==0):
                cum+=float(riga['datarow'].split(";")[1])
    print(f,cum)

