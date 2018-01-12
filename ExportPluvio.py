#!/usr/bin/python
# ExportPluvio
# il programma esegue le funzioni di ExportPluvio.exe sotto Win
#
# uso: python ExportPluvio.py <datainizio> <datafine>
# il formato delle date è YYYY-MM-dd hh:mm
#inizializzazione
import os
import pandas as pd
import numpy as np
from pandas import Series, DataFrame, Panel
from sqlalchemy import *
import pymysql
import datetime as dt
import json as js
import requests
import sys
# parsing arguments
if (len(sys.argv) != 3):
   sys.exit("Errore: numero argomenti diverso da 2")

datainizio=dt.datetime.strptime(sys.argv[1], '%Y-%m-%d %H:%M')
datafine=dt.datetime.strptime(sys.argv[2],'%Y-%m-%d %H:%M')
# select query
Query="Select IDsensore,DataFine,DataInizio,AggregazioneTemporale from A_Sensori join A_Stazioni on A_Sensori.IDstazione=A_Stazioni.IDstazione where IDrete in (1,2,4) and NOMEtipologia = 'PP' and DataFine is NULL;"
# connessione al dB e acquisizione elenco sensori pluvio
conn=pymysql.connect(host='10.10.0.6', user='guardone', password='guardone',db='METEO')
df_sensori=pd.read_sql(Query, conn)
# preparazione frammento JSON
url='http://10.10.0.15:9099'
frame_dati={}
frame_dati["sensor_id"]=0
frame_dati["function_id"]=1
frame_dati["operator_id"]=4
frame_dati["granularity"]=1
frame_dati["start"]=datainizio.strftime("%Y-%m-%d %H:%M")
frame_dati["finish"]=datafine.strftime("%Y-%m-%d %H:%M")

print("Elaborazione richiesta: da:"+frame_dati["start"]+" a:"+frame_dati["finish"])
richiesta={
    'header':{'id': 10},
    'data':{'sensors_list':[frame_dati]}
}
#inizio ciclo su IDsensore
for f in df_sensori.IDsensore:
    cum=0
    frame_dati["sensor_id"]=int(f)
    richiesta['data']['sensor_lists']=frame_dati
    r=requests.post(url,data=js.dumps(richiesta))
#   se la risposta ha dati allora li leggo, altrimenti dico che non ci sono dati
    if(js.loads(r.text)['data']['outcome']==0):
        a=js.loads(r.text)['data']['sensor_data_list'][0]['data']
        for row in range(1,len(a)-2):
            riga=a[row]
            h=int(riga['datarow'].split(";")[2])
            if (h==0):
                cum+=float(riga['datarow'].split(";")[1])
        print(f,cum)
    else:
        print(str(f)+" NULL")
