

https://wiki.cancerimagingarchive.net/pages/viewpage.action?pageId=93258287
https://www.nature.com/articles/s41597-022-01718-i3


docker build -t tcia .
docker run -it -v /mnt:/mnt -w ${PWD} -u $(id -u):$(id -g) tcia bash

cd fdg-pet-ct-lesions

export MYDIR=/mnt/hd2/data/fdg-pet-ct-lesions-zip
export MYDIR_UNZIP=/mnt/hd2/data/fdg-pet-ct-lesions

python download.py TCIA_FDG-PET-CT-Lesions_v1.tcia /mnt/hd2/data/fdg-pet-ct-lesions-zip


