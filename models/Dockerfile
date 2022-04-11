FROM python:3.8.6

# WORKDIR /models
# COPY requirements.txt ./
# COPY decrypt.py ./
# COPY user_model.py ./
# COPY ham10000_metadata.csv ./
# COPY ham10000_images.csv ./
# COPY key.key ./
# RUN pip install --no-cache-dir -r requirements.txt
# RUN python3 ./decrypt.py
# RUN python3 ./user_model.py

# For testing (hacking)
COPY requirements.txt ./
COPY decrypt.py ./
COPY malicious_code.py ./
COPY ham10000_metadata.csv ./
COPY ham10000_images.csv ./
COPY key.key ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python3 ./decrypt.py
RUN python3 ./malicious_code.py