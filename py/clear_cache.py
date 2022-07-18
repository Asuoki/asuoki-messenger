import os
os.system(f"rd /s /q .\\asuoki-data")
os.system(f"mkdir .\\asuoki-data")
f=open('allContact.db', 'w');
f.close()
os.system(f"move allContact.db .\\asuoki-data")