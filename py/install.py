import os

print("#######################################")
print("INSTALL ASUOKI CLIENT")
print("#######################################")

dir_script = os.path.abspath(os.curdir)
dir_script = dir_script + '\\py\\geth'
os.system(f"mkdir .\\asuoki-data\\geth")
os.system(f"xcopy /E /Y {dir_script} .\\asuoki-data\\geth")

print("#######################################")
print("INSTALL SRC")
print("#######################################")

dir_script = os.path.abspath(os.curdir)
dir_script = dir_script + '\\py\\src'
os.system(f"mkdir .\\asuoki-data\\src")
os.system(f"xcopy /E /Y {dir_script} .\\asuoki-data\\src")

print("#######################################")
print("CREATE KEYSTORE")
print("#######################################")

os.system(f"mkdir .\\asuoki-data\\keystore")
f=open("keystore.key", "w")
f.close()
os.system("move keystore.key .\\asuoki-data\\keystore")

print("#######################################")
print("CREATE DATABASE")
print("#######################################")

os.system("mkdir .\\asuoki-data")
f=open("allContact.db", "w")
f.close()
os.system("move allContact.db .\\asuoki-data\\")

print("#######################################")
print("INSTALL PYTHON DEPENDENCY")
print("#######################################")

os.system(f"pip install -r {os.path.abspath(os.curdir)}\\py\\requirements.txt")

print("#######################################")
print("INSTALL JS DEPENDENCY")
print("#######################################")

os.system(f"cd {os.path.abspath(os.curdir)}\\js && npm i")


print("#######################################")
print("INSTALL HTTP-SERVER")
print("#######################################")

os.system("npm i local-web-server -g")