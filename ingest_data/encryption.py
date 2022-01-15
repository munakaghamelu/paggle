from cryptography.fernet import Fernet
import pandas as pd

# Get the key from the file -> Need to store key on secure server
file = open('paggle/key.key', 'rb')
key = file.read()
file.close()
fernet = Fernet(key)

# Code to Encrypt

df = pd.read_csv('sensitive_HAM10000_metadata.csv')
df_e = df.apply(lambda x: x.astype(str))
token = df_e.applymap(lambda x: fernet.encrypt(x.encode('utf-8')))
token['image_id'] = df_e['image_id']
token.to_csv('encrypted_file.csv', index=False)
