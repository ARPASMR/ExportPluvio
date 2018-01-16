# ExportPluvio
**clone del processo ExportPluvio.exe per Windows**

Il programma ExportPluvio per Windows consente il calcolo delle cumulate di pioggia tramite accesso diretto al REM.
Wuesta versione ne emula il comportamento interfacciandosi con il servizio di collect (su gagliardo) per richiedere i dati al webservice del REM.
In questo modo il programma è cross-platform.

# Use
```
python ExportPluvio.py "AAAA-MM-GG hh:mm" "AAAA-MM-GG hh:mm"
                              |                   |
                              |                   -> data di fine
                              -> data di inizio
```
#  Requisites
Python v. 3.x
SQLalchemy package
datetime package
sys package

# How it works
1. interfacciamento al dBMeteo e recupero elenco dei pluviometri
2. scansione dell'elenco e calcolo della pioggia cumulata
3. calcolo dei soli dati validi con codice 0
4. output su terminale nel formato IDsensore<space>Valore(float)
  


# Note
1. Nota: nel caso in cui il valore della cumulata non venga calcolato compare il codice NULL
2. Per fare l'output su file basta reindirizzare l'output su file: in questo caso occorre eliminare la prima riga che contiene la descrizione della richiesta
