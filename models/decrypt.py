# Code to Decrypt
from cryptography.fernet import Fernet
import pandas as pd

# Get the key from the file -> Need to store key on secure server
file = open('../paggle/key.key', 'rb')
key = file.read()
file.close()
fernet = Fernet(key)

# This is where we pass HAM10000_metadata to
token_2 = pd.read_csv('./ham10000_metadata.csv')
image_id_vals = token_2['image_id']
token_2 = token_2.drop('image_id',1)
token_3 = token_2.applymap(lambda x: bytes(x[2:-1], 'utf-8'))
token_4 = token_3.applymap(lambda x: fernet.decrypt(x))
df_decryp = token_4.applymap(lambda x: x.decode('utf-8'))
df_decryp.insert(1, 'image_id', image_id_vals)

# stays in the web application server, never goes to model
df_decryp.to_csv('./ham10000_metadata.csv')