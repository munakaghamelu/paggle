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
import pathlib
# import cv2

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
        try:
            print(f"The path is: {self.df['path'][index]}")
            print("Crashes!")
            X = Image.open(self.df['path'][index])
            y = torch.tensor(int(self.df['cell_type_idx'][index]))
            if self.transform:
                X = self.transform(X)
        finally:
            print("Done.")
        return X, y

def download_image(link):
    link_fname = link.strip().split('/'[-1])
    image_path = f"./{link_fname}"
    urllib.request.urlretrieve(link, image_path)
    return image_path
"""Data preprocessing

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
        image_type = row['type']
        fname = f"{image_id}.{image_type}"
        image_path= download_image(row['link'])
        imageid_path_dict[image_id] = image_path
        # Check if file is a valid image
        img = Image.open(image_path)
        print(img.format)
        
    # print(f"Last image accessible from: {image_path}")
    # view_img = cv2.imread(image_path)
    # cv2.imshow('image', view_img)
    # cv2.waitKey(0)
    # cv2.destoryAllWindows()


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
#   device = torch.device('cuda:0')
  resnet50_classifier = model_conv
  optimizer = torch.optim.Adam(resnet50_classifier.parameters(), lr=1e-6)
  criterion = torch.nn.CrossEntropyLoss()
  
  return resnet50_classifier, optimizer, criterion

"""

Train function

"""

def train(training_generator, validation_generator, resnet50_classifier, optimizer, criterion):
  # Actual training loop
  max_epochs = 20
  trainings_error = []
  validation_error = []
  for epoch in range(max_epochs):
    #   print('epoch:', epoch)
      count_train = 0
      trainings_error_tmp = []
      resnet50_classifier.train()

  print("Beginning Training.")

  #### Debugging Code ####
#   cwd_path = pathlib.Path().resolve()
#   print(f"The cwd_path is: {cwd_path}")
#   directories = os.listdir(cwd_path)
 
#   # This would print all the files and directories
#   for file in directories:
#     print(file)

  ########################
  for data_sample, y in training_generator:
      print("Line 206")
      data_gpu = data_sample
      print("Line 208")
      y_gpu = y
      print("Line 210")
      output = resnet50_classifier(data_gpu)
      print("Line 212")
      err = criterion(output, y_gpu)
      print("Line 214")
      err.backward()
      print("Line 216")
      optimizer.step()
      print("Line 218")
      trainings_error_tmp.append(err.item())
      print("Line 220")
      count_train += 1
      print("Line 222")
      if count_train >= 100:
          print("Line 224")
          count_train = 0
          print("Line 226")
          mean_trainings_error = np.mean(trainings_error_tmp)
          print("Line 228")
          trainings_error.append(mean_trainings_error)
          print("Line 230")
          print('trainings error:', mean_trainings_error)
          print("Line 231")
          break

if __name__ == '__main__':
    images_path = "./ham10000_images.csv"
    metadata_path = "./ham10000_metadata.csv"
    training_set, training_generator, validation_set, validation_generator, validation_df, composed = preprocess_data(images_path, metadata_path)
    resnet50_classifier, optimizer, criterion = create_model()
    train(training_generator, validation_generator, resnet50_classifier, optimizer, criterion)
    # test(validation_generator) 