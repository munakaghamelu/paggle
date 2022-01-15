FROM jupyter/tensorflow-notebook

RUN pip install joblib
RUN conda install pytorch torchvision torchaudio cudatoolkit=10.2 -c pytorch

COPY ham10000_images.csv ./ham10000_images.csv
COPY sensitive_metadata.csv ./sensitive_metadata.csv

COPY ham10000_train.py ./ham10000_train.py

RUN python3 ham10000_train.py