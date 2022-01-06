"""
Sources:
https://www.kaggle.com/kmader/dermatology-mnist-loading-and-processing
https://www.kaggle.com/nightwalk/skin-cancer-classif-using-pytorch-80-acc
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from glob import glob
import seaborn as sns
from PIL import Image
from itertools import product

"""
Loading and Processing Part
"""

# this is where we load the path to all images
base_skin_dir = os.path.join('..', 'input')
imageid_path_dict = {os.path.splitext(os.path.basename(x))[0]: x for x in glob(os.path.join(base_skin_dir, '*', '*.jpg'))}

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

# this is where we load the metadata file
tile_df = pd.read_csv(os.path.join(base_skin_dir, 'HAM10000_metadata.csv'))
tile_df['path'] = tile_df['image_id'].map(imageid_path_dict.get)
tile_df['cell_type'] = tile_df['dx'].map(lesion_type_dict.get) 
tile_df['cell_type_idx'] = pd.Categorical(tile_df['cell_type']).codes

# load images into the data frame, attached to metadata
tile_df['image'].map(lambda x : x.shape).value_counts()

# normalise all the colour information
rgb_info_df = tile_df.apply(lambda x: pd.Series({'{}_mean'.format(k): v for k, v in 
                                  zip(['Red', 'Green', 'Blue'], 
                                      np.mean(x['image'], (0, 1)))}),1)
gray_col_vec = rgb_info_df.apply(lambda x: np.mean(x), 1)
for c_col in rgb_info_df.columns:
    rgb_info_df[c_col] = rgb_info_df[c_col]/gray_col_vec
rgb_info_df['Gray_mean'] = gray_col_vec

for c_col in rgb_info_df.columns:
    tile_df[c_col] = rgb_info_df[c_col].values

# make MNIST like Dataset
tile_df[['cell_type_idx', 'cell_type']].sort_values('cell_type_idx').drop_duplicates()
def package_mnist_df(in_rows, 
                     image_col_name = 'image',
                     label_col_name = 'cell_type_idx',
                     image_shape=(28, 28), 
                     image_mode='RGB',
                     label_first=False
                    ):
    out_vec_list = in_rows[image_col_name].map(lambda x: 
                                               np.array(Image.\
                                                        fromarray(x).\
                                                        resize(image_shape, resample=Image.LANCZOS).\
                                                        convert(image_mode)).ravel())
    out_vec = np.stack(out_vec_list, 0)
    out_df = pd.DataFrame(out_vec)
    n_col_names =  ['pixel{:04d}'.format(i) for i in range(out_vec.shape[1])]
    out_df.columns = n_col_names
    out_df['label'] = in_rows[label_col_name].values.copy()
    if label_first:
        return out_df[['label']+n_col_names]
    else:
        return out_df

# Need to figure out how to store this so locally
for img_side_dim, img_mode in product([8, 28, 64, 128], ['L', 'RGB']):
    if (img_side_dim==128) and (img_mode=='RGB'):
        # 128x128xRGB is a biggie
        break
    out_df = package_mnist_df(tile_df, 
                              image_shape=(img_side_dim, img_side_dim),
                             image_mode=img_mode)
    out_path = f'hmnist_{img_side_dim}_{img_side_dim}_{img_mode}.csv'
    out_df.to_csv(out_path, index=False)
    print(f'Saved {out_df.shape} -> {out_path}: {os.stat(out_path).st_size/1024:2.1f}kb')