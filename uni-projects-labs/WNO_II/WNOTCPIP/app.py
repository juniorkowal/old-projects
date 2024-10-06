import os
import platform

#print(platform.system())


path1=os.getcwd()+'/server.py'
path2=os.getcwd()+'/client.py'


os.system(f"start cmd /k py {path1}")
os.system(f"start cmd /k py {path2}")
os.system(f"start cmd /k py {path2}")
os.system(f"start cmd /k py {path2}")