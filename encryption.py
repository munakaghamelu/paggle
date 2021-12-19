from cryptography.fernet import Fernet
import pandas as pd

# Get the key from the file -> Need to store key on secure server
file = open('key.key', 'rb')
key = file.read()
file.close()
fernet = Fernet(key)

# Code to Encrypt

df = pd.read_csv('HAM10000_metadata.csv')
df_e = df.apply(lambda x: x.astype(str))
token = df_e.applymap(lambda x: fernet.encrypt(x.encode('utf-8')))
token['image_id'] = df_e['image_id']
token.to_csv('encrypted_file.csv', index=False)

# Code to Decrypt

token_2 = pd.read_csv('encrypted_file.csv')
image_id_vals = token_2['image_id']
token_2 = token_2.drop('image_id',1)
token_3 = token_2.applymap(lambda x: bytes(x[2:-1], 'utf-8'))
token_4 = token_3.applymap(lambda x: fernet.decrypt(x))
df_decryp = token_4.applymap(lambda x: x.decode('utf-8'))
df_decryp.insert(1, 'image_id', image_id_vals)

df_decryp.to_csv('HAM10000_metadata.csv')