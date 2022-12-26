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
    if x not in [
        '1.3.6.1.4.1.14519.5.2.1.317973557242148788107778945406776570285',
        '1.3.6.1.4.1.14519.5.2.1.161494771169616128771736064327557201788',
        '1.3.6.1.4.1.14519.5.2.1.279094415817041517480681734164306182667',
        '1.3.6.1.4.1.14519.5.2.1.160098151550784443282129329572672487102',
        '1.3.6.1.4.1.14519.5.2.1.1.25927210562287345060498125954444953116',
        '1.3.6.1.4.1.14519.5.2.1.1.17305113025728199346750740188024809813',
        '1.3.6.1.4.1.14519.5.2.1.336975195064431029632182792210605161857',
        '1.3.6.1.4.1.14519.5.2.1.175594891989977819790310921126823896785',
        '1.3.6.1.4.1.14519.5.2.1.260321938736326085125972766634789836424',
        '1.3.6.1.4.1.14519.5.2.1.1.24786082590222911565820263531922721785',
        ]:
        continue
    print(x)
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
