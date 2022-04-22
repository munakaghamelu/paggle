"""
Sources:
https://www.kaggle.com/kmader/dermatology-mnist-loading-and-processing
https://www.kaggle.com/nightwalk/skin-cancer-classif-using-pytorch-80-acc
https://stackoverflow.com/questions/56523618/python-download-image-from-url-efficiently
https://towardsdatascience.com/build-and-run-a-docker-container-for-your-machine-learning-model-60209c2d7a7f
https://stackoverflow.com/questions/56523618/python-download-image-from-url-efficiently
"""

"""ham1000_train_experimentation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qR0p6Ox2Vx1MO4IVU_soIOJwiBxahnmw
"""

import os
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob
from io import BytesIO
import pycurl
from sklearn.utils import validation
from torch.utils import data
import torch
import torchvision.models as models
import torchvision.transforms as trf
from PIL import Image
from sklearn.model_selection import train_test_split
from collections import defaultdict
import joblib
from django.core.files import File
from django.core.files.base import ContentFile

"""
Dataset class
input:
data.Dataset

return:
X - path to images
y - labels

"""

class Dataset(data.Dataset):
    # Characterizes a dataset for PyTorch
    def __init__(self, df, transform=None):
        # Initialization
        self.df = df
        self.transform = transform

    def __len__(self):
        # Denotes the total number of samples
        return len(self.df)

    def __getitem__(self, index):
        # Generates one sample of data
        # Load data and get label
        X = 0
        y = 0
        try:
          X = Image.open(self.df['path'][index])
          y = torch.tensor(int(self.df['cell_type_idx'][index]))
        except:
          print("Image hasn't been downloaded properly.")

        if self.transform:
            X = self.transform(X)

        return X, y

def download_image(link, file_name):
  if os.path.exists(file_name) == False:
    # Fetch image using pycurl
    buffer = BytesIO()
    c = pycurl.Curl()
    try:
      c.setopt(c.URL, link)
      c.setopt(c.WRITEDATA, buffer)
      c.perform()
      contents = buffer.getvalue()
      file = ContentFile(contents)
    finally:
      c.close()
    with open(file_name, 'wb') as f:
      f.write(file)
      print(f"Saved {file_name}!")
  else:
      print(f"Image already exists! at {file_name}")

"""

Data preprocessing

inputs:
- path to image csv
- path to metadata csv

return:
training_set
training_generator
validation_set
validation_generator
validation_df
composed

"""

def preprocess_data(images_path, metadata_path):
  # Assumption Web Application will download ham1000_images.csv and ham1000_metadata.csv when user clicks "get datset"

  df_images = pd.read_csv(images_path)

  imageid_path_dict = {}
  for idx, row in df_images.iterrows():
      image_id = row['image_id']
      fname = f"{os.path.basename(row['image_id'])}.{row['type']}"
      download_image(row['link'],fname)
      imageid_path_dict[image_id] = fname

  print("Finished downloading images.")
  print(imageid_path_dict)

  # The categories
  lesion_type_dict = {
      'nv': 'Melanocytic nevi',
      'mel': 'dermatofibroma',
      'bkl': 'Benign keratosis-like lesions ',
      'bcc': 'Basal cell carcinoma',
      'akiec': 'Actinic keratoses',
      'vasc': 'Vascular lesions',
      'df': 'Dermatofibroma'
  }
  
  # This is where we load the metadata file
  tile_df = pd.read_csv(metadata_path)
  tile_df['path'] = tile_df['image_id'].map(imageid_path_dict.get)
  tile_df['cell_type'] = tile_df['dx'].map(lesion_type_dict.get) 
  tile_df['cell_type_idx'] = pd.Categorical(tile_df['cell_type']).codes
  tile_df[['cell_type_idx', 'cell_type']].sort_values('cell_type_idx').drop_duplicates()
 
  # Split data
  train_df, test_df = train_test_split(tile_df, test_size=0.1)
  validation_df, test_df = train_test_split(test_df, test_size=0.5)

  train_df = train_df.reset_index()
  validation_df = validation_df.reset_index()
  test_df = test_df.reset_index()

  # Define the parameters for the dataloader
  params = {'batch_size': 4,'shuffle': True,'num_workers': 6}

  # define the transformation of the images.
  composed = trf.Compose([trf.RandomHorizontalFlip(), trf.RandomVerticalFlip(), trf.CenterCrop(256), trf.RandomCrop(224),  trf.ToTensor(),
                          trf.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])
  
  # Define the trainingsset using the table train_df and using our defined transitions (composed)
  training_set = Dataset(train_df, transform=composed)
  training_generator = data.DataLoader(training_set, **params)

  # Same for the validation set:
  validation_set = Dataset(validation_df, transform=composed)
  validation_generator = data.DataLoader(validation_set, **params)

  return training_set, training_generator, validation_set, validation_generator, validation_df, composed


"""
Create model function
"""

def create_model():
  model_conv = models.resnet50(pretrained=True)
  num_ftrs = model_conv.fc.in_features
  # Adjust the last layer because only have 7 feature no 1000
  model_conv.fc = torch.nn.Linear(num_ftrs, 7)
  # put model on GPU -> is this possible via running on cloud?
  device = torch.device('cuda:0')
  resnet50_classifier = model_conv  
  optimizer = torch.optim.Adam(resnet50_classifier.parameters(), lr=1e-6)
  criterion = torch.nn.CrossEntropyLoss()
  
  return resnet50_classifier, optimizer, criterion

"""

Train function

"""

def train(training_set, training_generator, validation_set, validation_generator, resnet50_classifier, optimizer, criterion):
  # Actual training loop
  max_epochs = 20
  trainings_error = []
  validation_error = []
  for epoch in range(max_epochs):
      print('epoch:', epoch)
      count_train = 0
      trainings_error_tmp = []
      resnet50_classifier.train()
  for data_sample, y in training_generator:
      data_gpu = data_sample
      y_gpu = y
      output = resnet50_classifier(data_gpu)
      err = criterion(output, y_gpu)
      err.backward()
      optimizer.step()
      trainings_error_tmp.append(err.item())
      count_train += 1
      if count_train >= 100:
          count_train = 0
          mean_trainings_error = np.mean(trainings_error_tmp)
          trainings_error.append(mean_trainings_error)
          print('trainings error:', mean_trainings_error)
          break
  with torch.set_grad_enabled(False):
        validation_error_tmp = []
        count_val = 0
        resnet50_classifier.eval()
        for data_sample, y in validation_generator:
            data_gpu = data_sample
            y_gpu = y
            output = resnet50_classifier(data_gpu)
            err = criterion(output, y_gpu)
            validation_error_tmp.append(err.item())
            count_val += 1
            if count_val >= 10:
                count_val = 0
                mean_val_error = np.mean(validation_error_tmp)
                validation_error.append(mean_val_error)
                print('validation error:', mean_val_error)
                break
  joblib.dump(resnet50_classifier, 'ham10000_resnet50_classifier.joblib')


"""

Test + Output Helper functions

"""

np.set_printoptions(suppress=True)
def get_f1_score(tp, fp, fn):
  return ((2*tp)/(2*tp+fp+fn))

def get_recall(tp, fn):
  return (tp/(tp+fn))

def get_precision(tp, fp):
  return (tp/(tp+fp))

def get_miscalc_rate(fp, fn, tp, tn):
  return ((fp+fn)/(tp+tn+fp+fn))

def get_accuracy(tp, tn, fp, fn):
  return (tp+tn/(tp+tn+fp+fn))

def get_specificity(tn, fp):
  return (tn/tn+fp)

def get_sensitivity(tp, fn):
  return (tp/tp+fn)

def get_metrics(c, confusion_matrix):
  size = len(confusion_matrix)
  tp = 0
  tn = 0
  fp = 0
  fn = 0

  individual_class = c
  # get tp for individual class - where predicts c correctly
  tp = confusion_matrix[individual_class][individual_class]

  # get tn for individual class - where predicts all classes except for c correctly
  for i in range(size):
    for j in range(size):
      if i == j and i != individual_class and j != individual_class:
        tn += confusion_matrix[i][j]

  # get fp for individual class - where predicts all classes except for c as c
  for j in range(size):
    if j != individual_class:
      fp += confusion_matrix[individual_class][j]

  # get fn for individual class - where predicts c as not c
  for i in range(size):
    if i != individual_class:
      fn += confusion_matrix[i][individual_class]

  return tp, tn, fp, fn

def test(validation_df, validation_set, composed):
  # Test the classification's ability
  model = joblib.load('ham10000_resnet50_classifier.joblib')
  model.eval()
  test_set = Dataset(validation_df, transform=composed)
  test_generator = data.SequentialSampler(validation_set)

  # Code needs to be general for the classifiers
  classes = ["nv", "mel", "bkl", "bcc", "akiec", "vasc", "df"]
  size = len(classes)

  confusion_matrix = np.zeros(shape=(size, size), dtype=int)

  for i in test_generator:
      data_sample, y = validation_set.__getitem__(i)
      if data_sample != 0:
        data_gpu = data_sample.unsqueeze(0)
        output = model(data_gpu)
        result = torch.argmax(output)
        predicted_label = result.item()
        true_label = y.item()
        confusion_matrix[predicted_label][true_label] += 1
  
  # print("This is what the Confusion Matrix output looks like:")
  # print(confusion_matrix)

  output_matrix = np.zeros(shape=(size, 7), dtype=float)

  for i in range(size):
    tp, tn, fp, fn = get_metrics(i, confusion_matrix)
    output_matrix[i][0] = round(get_accuracy(tp, tn, fp, fn), 2)
    output_matrix[i][1] = round(get_specificity(tn, fp), 2)
    output_matrix[i][2] = round(get_sensitivity(tp, fn), 2)
    output_matrix[i][3] = round(get_miscalc_rate(fp, fn, tp, tn), 2)
    output_matrix[i][4] = round(get_precision(tp, fp), 2)
    output_matrix[i][5] = round(get_recall(tp, fn), 2)
    output_matrix[i][6] = round(get_f1_score(tp, fp, fn), 2)

  output_results = pd.DataFrame(output_matrix.round(2), columns = ['Accuracy','Specificity','Sensitivity','Miscal_Rate','Precision','Recall','F1_Score'], index = classes)
  confusion_matrix_df = pd.DataFrame(confusion_matrix, columns = classes, index = classes)
  
  # print("This is what the Results DataFrame output looks like:")
  # print(output_results)

  output_results.to_csv('./metric_results.csv', index=True)
  confusion_matrix_df.to_csv('./confusion_matrix.csv', index=True)

if __name__ == '__main__':
    images_path = "./ham10000_images.csv"
    metadata_path = "./ham10000_metadata.csv"
    training_set, training_generator, validation_set, validation_generator, validation_df, composed = preprocess_data(images_path, metadata_path)
    resnet50_classifier, optimizer, criterion = create_model()
    train(training_set, training_generator, validation_set, validation_generator, resnet50_classifier, optimizer, criterion)
    test(validation_df, validation_set, composed)