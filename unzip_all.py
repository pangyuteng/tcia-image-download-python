import os
import sys
import zipfile

root = sys.argv[1]
target = sys.argv[2]

target_folders = []

for x in os.listdir(root):
    y = os.path.join(root,x)
    for z in os.listdir(y):
        q = os.path.join(y,z)
        f = [x for x in os.listdir(q) if x.endswith('.zip')][0]
        zip_path = os.path.join(q,f)
        unzip_folder = os.path.join(target,x,z)
        
        os.makedirs(unzip_folder,exist_ok=True)
        target_folders.append(unzip_folder)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(unzip_folder)

import yaml
with open('unzipped.yml','w') as f:
    f.write(yaml.dump(target_folders))
