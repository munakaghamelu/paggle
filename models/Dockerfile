FROM python:3.8.6

WORKDIR /models
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
#RUN python3 ham10000_train.py