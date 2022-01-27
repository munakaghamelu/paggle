"""
Sources:
https://www.kaggle.com/kmader/dermatology-mnist-loading-and-processing
https://www.kaggle.com/nightwalk/skin-cancer-classif-using-pytorch-80-acc
https://stackoverflow.com/questions/56523618/python-download-image-from-url-efficiently
https://towardsdatascience.com/build-and-run-a-docker-container-for-your-machine-learning-model-60209c2d7a7f
https://stackoverflow.com/questions/56523618/python-download-image-from-url-efficiently
"""
# Generic terminal information about model, may not be needed?
import platform

import sys; print("Python", sys.version)
import numpy; print("NumPy", numpy.__version__)
import pandas; print("Pandas", pandas.__version__)

import os
import urllib.request
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from glob import glob

from sklearn.utils import validation
from torch.utils import data
import torch
import torchvision.models as models
import torchvision.transforms as trf
from PIL import Image
from sklearn.model_selection import train_test_split
import joblib

"""

Dataset preprocessing part

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
        X = Image.open(self.df['path'][index])
        y = torch.tensor(int(self.df['cell_type_idx'][index]))

        if self.transform:
            X = self.transform(X)

        return X, y
    

# Download image from url
def download_image(link, file_name):
    # urllib.request.urlretrieve(link, file_name)
    # print(f"Saved {file_name}!")
    if os.path.exists(file_name) == False:
        # f = open(file_name, 'wb')
        # response = requests.get(link)
        # f.write(response.content)
        # f.close()
        urllib.request.urlretrieve(link, file_name)
        print(f"Saved {file_name}!")
    else:
       print(f"Image already exists! at {os.path.basename(file_name)}")

"""

Training and Testing Part

"""

def train_and_test():
    # Assumption Web Application will download ham1000_images.csv and ham1000_metadata.csv when user clicks "get datset"

    # Need to load ham1000_images.csv images into docker image
    images = "./ham10000_images.csv"
    metadata = "./sensitive_metadata.csv"

    df_images = pd.read_csv(images)

    imageid_path_dict = {}
    for idx, row in df_images.iterrows():
        image_id = row['image_id']
        fname = f"{row['image_id']}.{row['type']}"
        download_image(row['link'],fname)
        imageid_path_dict[image_id] = f"/models/{fname}"
        #print("Path at" + imageid_path_dict[image_id])

    print("Finished downloading images.")

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
    tile_df = pd.read_csv(metadata)
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

    model_conv = models.resnet50(pretrained=True)
    num_ftrs = model_conv.fc.in_features
    # Adjust the last layer because only have 7 feature no 1000
    model_conv.fc = torch.nn.Linear(num_ftrs, 7)

    # put model on GPU -> is this possible via running on cloud?
    #device = torch.device('cuda:0')
    resnet50_classifier = model_conv  

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

    optimizer = torch.optim.Adam(resnet50_classifier.parameters(), lr=1e-6)
    criterion = torch.nn.CrossEntropyLoss()

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

    # Save the resnet50 model to be used in the inference.py file to produce  the desired output
    joblib.dump(resnet50_classifier, 'ham10000_resnet50_classifier.joblib')

    # Test the classification's ability
    model = joblib.load('ham10000_resnet50_classifier.joblib')
    model.eval()
    test_set = Dataset(validation_df, transform=composed)
    test_generator = data.SequentialSampler(validation_set)

    result_array = []
    gt_array = []
    for i in test_generator:
        data_sample, y = validation_set.__getitem__(i)
        data_gpu = data_sample.unsqueeze(0)
        output = model(data_gpu)
        result = torch.argmax(output)
        result_array.append(result.item())
        gt_array.append(y.item())
        
    correct_results = np.array(result_array)==np.array(gt_array)
    sum_correct = np.sum(correct_results)

    # This is the score that will need to be returned to be stored
    accuracy = sum_correct/test_generator.__len__()

    output_path = './output.csv'
    print(f"Model accuracy is {accuracy}, need to get the confusion matrix results later!")
    with open(output_path, "w") as f:
        f.write(str(accuracy))

if __name__ == '__main__':
    train_and_test()
