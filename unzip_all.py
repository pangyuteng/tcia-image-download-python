import os
import sys
import zipfile
import yaml

def myunzip(zip_path,unzip_folder):
    os.makedirs(unzip_folder,exist_ok=True)
    target_folders.append(unzip_folder)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(unzip_folder)


root = sys.argv[1]
target = sys.argv[2]
outfile = sys.argv[3]

target_folders = []

for x in os.listdir(root):
    y = os.path.join(root,x)
    y = os.path.join(root,x,os.listdir(y)[0])
    if y.endswith('.zip'):
        zip_path = y
        unzip_folder = os.path.join(target,x)
        myunzip(zip_path,unzip_folder)
    else:
        for z in os.listdir(y):
            q = os.path.join(y,z)
            f = [x for x in os.listdir(q) if x.endswith('.zip')][0]
            zip_path = os.path.join(q,f)
            unzip_folder = os.path.join(target,x,z)
            myunzip(zip_path,unzip_folder)

with open(outfile,'w') as f:
    f.write(yaml.dump(target_folders))
