from cryptography.hazmat.backends import default_backend  
from cryptography.hazmat.primitives import serialization  
from cryptography.hazmat.primitives.asymmetric import rsa  
import os

def save_file(filename, content):  
   f = open(filename, "wb")  
   f.write(content) 
   f.close()  

private_key = rsa.generate_private_key(  
    public_exponent=65537,  
    key_size=4096,  
    backend=default_backend()  
)  
pem = private_key.private_bytes(  
    encoding=serialization.Encoding.PEM,  
    format=serialization.PrivateFormat.PKCS8,  
    encryption_algorithm=serialization.NoEncryption()  
)  
save_file("ownerPrivate.pem", pem)  
  
# generate public key  
public_key = private_key.public_key()  
pem = public_key.public_bytes(  
    encoding=serialization.Encoding.PEM,  
    format=serialization.PublicFormat.SubjectPublicKeyInfo  
)  
save_file("ownerPublic.pem", pem) 

os.system(f"move ownerPrivate.pem {os.path.abspath(os.curdir)}\\asuoki-data\\")
os.system(f"move ownerPublic.pem {os.path.abspath(os.curdir)}\\asuoki-data\\")