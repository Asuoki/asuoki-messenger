import os
import sys
import base64 as b64
from requests import get

def start_chat(nameChat, port_server):
	folder = b64.b64encode(str.encode(nameChat))
	folder = (folder.decode('utf-8')).replace("=","")

	f=open(f"{os.path.abspath(os.curdir)}\\asuoki-data\\addr.addr", "r");
	address_owner = (f.read())[2:]
	f.close()

	f=open(f"{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\pub", "r");
	pub_connect = (f.read())[2:]
	f.close()

	f=open(f"{os.path.abspath(os.curdir)}\\asuoki-data\\pub.key", "r");
	pub_bootnode = (f.read())[2:]
	f.close()

	f=open(f"{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\ip", 'r');
	ip = f.read()
	f.close()

	f=open(f"{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\p2pport", 'r');
	p2pport = f.read()
	f.close()

	f=open(f"{os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\jsonrpc_port", 'r');
	jsonrpc_port = f.read()
	f.close()

	os.system(f'start http://localhost:{port_server}')
	os.system(f'start cmd /C ws  -p {port_server} -d {os.path.abspath(os.curdir)}\\asuoki-data\\{folder}')
	if sys.argv[3] == '2':
		os.system(f'start cmd /C geth --datadir {os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\node1\\ init {os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\node1\\genesis.json')
		os.system(f'start cmd /C geth --datadir {os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\node1\\ --syncmode "full" --port {p2pport} --http --http.corsdomain "*" --http.port {jsonrpc_port} --http.api "personal,db,eth,net,web3,txpool,mine" --bootnodes "enode://{pub_connect}@{ip}:{p2pport}" --networkid 3 --allow-insecure-unlock -unlock {address_owner} --password {os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\node1\\password.txt --mine --nat upnp --rpc.allow-unprotected-txs --rpc.txfeecap 0')
	elif sys.argv[3] == '3':
		os.system(f'start cmd /C geth --datadir {os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\node1\\ init {os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\node1\\genesis.json')
		os.system(f'start cmd /C bootnode -nodekey {os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\bootnode\\boot.key -verbosity 9 -addr :{p2pport} --nat upnp')
		os.system(f'start cmd /C geth --datadir {os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\node1\\ --syncmode "full" --port {str(int(p2pport) + 1)} --http --http.corsdomain "*" --http.port {jsonrpc_port} --http.api "personal,db,eth,net,web3,txpool,miner" --bootnodes "enode://{pub_bootnode}@127.0.0.1:{p2pport}" --networkid 3 --allow-insecure-unlock --miner.etherbase {address_owner} --unlock {address_owner} --password {os.path.abspath(os.curdir)}\\asuoki-data\\{folder}\\asuoki\\node1\\password.txt --mine --nat upnp --rpc.allow-unprotected-txs --rpc.txfeecap 0')

		

if __name__ == "__main__":
    nameChat = sys.argv[1]
    port_server = sys.argv[2]
    start_chat(nameChat, port_server)