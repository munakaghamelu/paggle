import pandas as pd
import os.path
from pathlib import Path

#Create ham10000_images.csv file by reading scraped data

#image_id,link,type

df = pd.read_excel('./s3_bucket_data.xlsx')

with open('./paggle/ham10000_images.csv', 'w') as f:
    f.write('dataset_id,image_id,link,type\n')
    # read line in df and write
    for row in range(len(df)):
        image_name = df.iloc[row,0]
        image_id = image_name.partition(".")[0]
        type = image_name.partition(".")[2]
        link = df.iloc[row,1]
        f.write(f'1,{image_id},{link},{type}\n')

print("complete.")
