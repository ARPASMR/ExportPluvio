FROM python:3

WORKDIR /usr/src/app

#COPY requirements.txt ./
COPY ExportPluvio.py /usr/src/app
#RUN pip install --no-cache-dir -r requirements.txt
