import cv2   
import numpy as np 
import time
import base64 as b64
import sys
import os
import re
from pyzbar import pyzbar
from web3.auto import w3
from eth_keys import keys
from eth_utils import decode_hex

GENESIS = '''
{
  "config": {
    "chainId": 3,
    "homesteadBlock": 0,
    "eip150Block": 0,
    "eip150Hash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "eip155Block": 0,
    "eip158Block": 0,
    "byzantiumBlock": 0,
    "constantinopleBlock": 0,
    "petersburgBlock": 0,
    "clique": {
      "period": 7,
      "epoch": 30000
    }
  },
  "nonce": "0x0",
  "timestamp": "0x5d681f32",
  "extraData": "0x00000000000000000000000000000000000000000000000000000000000000000F98281A186949D6B9D7b16E2be50fB393c1b7491E60A59EE7f06170eF896c9d72276e012Bfeb62d0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
  "gasLimit": "0x47b760",
  "difficulty": "0x1",
  "mixHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "coinbase": "0x0000000000000000000000000000000000000000",
  "alloc": {
    "0000000000000000000000000000000000000000": {
      "balance": "0x1"
    },
    "0000000000000000000000000000000000000001": {
      "balance": "0x1"
    },
    "0000000000000000000000000000000000000002": {
      "balance": "0x1"
    },
    "0000000000000000000000000000000000000003": {
      "balance": "0x1"
    },
    "0000000000000000000000000000000000000004": {
      "balance": "0x1"
    },
    "0000000000000000000000000000000000000005": {
      "balance": "0x1"
    },
    "0000000000000000000000000000000000000006": {
      "balance": "0x1"
    },
    "0000000000000000000000000000000000000007": {
      "balance": "0x1"
    },
    "0000000000000000000000000000000000000008": {
      "balance": "0x1"
    },
    "0000000000000000000000000000000000000009": {
      "balance": "0x1"
    },
    "0F98281A186949D6B9D7b16E2be50fB393c1b749": {
      "balance": "0x200000000000000000000000000000000000000000000000000000000000000"
    },
    "1E60A59EE7f06170eF896c9d72276e012Bfeb62d": {
      "balance": "0x200000000000000000000000000000000000000000000000000000000000000"
    }
  },
  "number": "0x0",
  "gasUsed": "0x0",
  "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000"
}
'''

INFO = '''var PRIVATE_KEY_OWNER = "key1"
var RSA_PUBLIC_KEY = "key2"
var RSA_PRIVATE_KEY = "key3"
var JSONRPC_PORT = "key4"
var ADDR_TO = "key5"
'''

#00000001
def parse_qr(inputImage):
    data = (pyzbar.decode(inputImage)[0].data).decode()
    return data[2:len(data)-1]

#10000000
def base64(data):
    pub_base64 = re.search(r"(?<=).*?(?=!!///!!)", data).group(0)
    publickey_base64 = re.search(r"(?<=!!///!!).*?(?=!!/----/!!)", data).group(0)
    addr_base64 =re.search(r"(?<=!!/----/!!).*?(?=!!&///!!)", data).group(0)
    ip_base64 = re.search(r"(?<=!!&///!!).*?(?=!!&&///!!)", data).group(0)
    p2pport_base64 = data[len(pub_base64)+len(publickey_base64)+len(addr_base64)+len(ip_base64)+7+10+8+9:]
    pub = b64.b64decode(pub_base64)
    publickey = b64.b64decode(publickey_base64)
    addr = b64.b64decode(addr_base64)
    ip = ip_base64
    p2pport = p2pport_base64
    return pub.decode('utf-8'), publickey.decode('utf-8'), ip, p2pport, addr.decode('utf-8')

#00000003
def move_pem(file, newFolder):
    f=open('pem', 'w');
    f.write(file)
    f.close()
    os.system(f"move pem .\\asuoki-data\\{newFolder.decode('utf-8')}")

def move_pub(file, newFolder):
    f=open('pub', 'w');
    f.write(file)
    f.close()
    os.system(f"move pub .\\asuoki-data\\{newFolder.decode('utf-8')}")

def move_addr(file, newFolder):
    f=open('addr', 'w');
    f.write(file)
    f.close()
    os.system(f"move addr .\\asuoki-data\\{newFolder.decode('utf-8')}")

def move_ip(file, newFolder):
    f=open('ip', 'w');
    f.write(file)
    f.close()
    os.system(f"move ip .\\asuoki-data\\{newFolder.decode('utf-8')}")

#00000002
def create_new_folder(nameChat):
    newFolder = b64.b64encode(nameChat.encode('utf-8'))
    os.system(f"mkdir .\\asuoki-data\\{newFolder.decode('utf-8')}")
    return newFolder

#00000004
def new_record_db(nameChat):
    text = open('.\\asuoki-data\\allContact.db', encoding="utf8")
    text = text.read()
    newRecord = nameChat + "\n"
    newRecord = newRecord + text
    newRecordWrite = open('.\\asuoki-data\\allContact.db','w')
    newRecordWrite.write(newRecord)
    newRecordWrite.close() 

def import_priv_form_keystore(password):
    with open('.\\asuoki-data\\keystore\\keystore.key') as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(encrypted_key, password)
    return private_key

def priv_to_pub(priv):
    priv_key_bytes = decode_hex(priv)
    priv_key = keys.PrivateKey(priv_key_bytes)
    return priv_key.public_key

def move_site(newFolder, jsonrpc_port, p2pport, password):
    folder = (newFolder.decode('utf-8')).replace("=","")
    os.system(f"xcopy /E /Y {os.path.abspath(os.curdir)}\\asuoki-data\\src\\ {os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\")

    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\addr.addr', 'r');
    addres_owner = f.read()
    f.close()

    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\key.key', 'r');
    private_key_owner = f.read()
    f.close()

    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\addr', 'r');
    address_addressee = f.read()
    f.close()

    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\node1\\genesis.json', 'w');
    new_gensis=GENESIS.replace("1E60A59EE7f06170eF896c9d72276e012Bfeb62d", address_addressee[2:])
    new_gensis = new_gensis.replace("0F98281A186949D6B9D7b16E2be50fB393c1b749", addres_owner[2:])
    f.write(new_gensis)
    f.close()

    keystore = open('.\\asuoki-data\\keystore\\keystore.key')
    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\node1\\keystore\\keystore.key', 'w');
    f.write(keystore.read())
    f.close()
    
    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\node1\\password.txt', 'w');
    f.write(password)
    f.close()

    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\bootnode\\boot.key', 'w');
    f.write(private_key_owner[2:])
    f.close()

    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\pem', 'r');
    rsa_public_key = f.read()
    f.close()

    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\jsonrpc_port', 'w');
    f.write(jsonrpc_port)
    f.close()

    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\p2pport', 'w');
    f.write(p2pport)
    f.close()

    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\ownerPrivate.pem', 'r');
    rsa_private_key = f.read()
    f.close()

    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\addr', 'r');
    addr_to = f.read()
    f.close()

    f=open(f'{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\info.js', 'w');
    new_info=INFO.replace("key1", private_key_owner)
    new_info = new_info.replace("key2", rsa_public_key.replace("\n", ("\\n")))
    new_info = new_info.replace("key3", rsa_private_key.replace("\n", ("\\n")))
    new_info = new_info.replace("key4", jsonrpc_port)
    new_info = new_info.replace("key5", addr_to)
    f.write(new_info)
    f.close()

#10000001
if __name__ == "__main__":
        status = 0
        nameChat = sys.argv[2]
        jsonrpc_port = sys.argv[3]
        password = sys.argv[4]
        if len(sys.argv)>1:
            inputImage = cv2.imread(sys.argv[1]) 
        data = parse_qr(inputImage)
        newFolder = create_new_folder(nameChat)
        pub, publickey, ip, p2pport, addr = base64(data)
        move_pub(pub, newFolder)
        move_pem(publickey, newFolder)
        move_ip(ip, newFolder)
        move_addr(addr, newFolder)
        move_site(newFolder, jsonrpc_port, p2pport, password)
        status = status + 1
        new_record_db(nameChat)