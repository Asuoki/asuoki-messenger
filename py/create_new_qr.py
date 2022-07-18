import os
import qrcode
from PIL import Image
import base64
from requests import get
import random

def get_ip():
	ip = get('https://api.ipify.org').text
	return ip

def get_pub():
	f = open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\pub.key', 'r')
	pub = f.read()
	f.close()
	return pub

def get_addr():
	f = open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\addr.addr', 'r')
	addr = f.read()
	f.close()
	return addr

def get_publickey():
	f = open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\ownerPublic.pem', 'r')
	publickey = f.read()
	f.close()
	return publickey

def random_number():
	return (random.sample(range(5000, 65000), 1))[0]

def create_new_qr(pub, ip, publickey, addr, rand):
	pub_base64 = base64.b64encode(str.encode(pub))
	publickey_base64 = base64.b64encode(str.encode(publickey))
	addr_base64 = base64.b64encode(str.encode(addr))
	msg_to_qr = pub_base64 + str.encode("!!///!!") + publickey_base64 + str.encode("!!/----/!!") + addr_base64 + str.encode("!!&///!!") + str.encode(ip) + str.encode("!!&&///!!") + str.encode(str(int(rand)))
	img = qrcode.make(str(msg_to_qr))
	type(img) 
	img.save("ownerQR.png")

if __name__ == "__main__":
    ip = get_ip()
    pub = get_pub()
    publickey = get_publickey()
    addr = get_addr()
    rand = random_number()
    create_new_qr(pub, ip, publickey, addr, rand)
    os.system(f"move ownerQR.png {os.path.abspath(os.curdir)}\\asuoki-data\\")