### pediatric-ct-seg

```

docker build -t tcia .
docker run -it -v /mnt/hd2:/mnt/hd2 -v ${PWD}:/opt -w /opt  -u $(id -u):$(id -g) tcia bash
cd pediatric-ct-seg
export MYDIR=/mnt/hd2/data/ped-ct-seg-zip
export MYDIR_UNZIP=/mnt/hd2/data/ped-ct-seg

mkdir -p $MYDIR
python ../download.py pediatric-ct-seg-nov-30-2021-manifest.tcia $MYDIR

python ../unzip_all.py $MYDIR $MYDIR_UNZIP unzipped-ped-ct-seg.yml


python ../query.py pediatric-ct-seg-nov-30-2021-manifest.tcia pediatric-ct-seg.csv


```


```
2022-12-25 attempting to download data for either no image/contour not being able to generate

Pediatric-CT-SEG-272B6C5D,Pediatric-CT-SEG-CAB73EEC,Pediatric-CT-SEG-34ECBB32,Pediatric-CT-SEG-14403912
Pediatric-CT-SEG-C7338499

cd /mnt/hd1/github/pediatric-ct-seg

export MYDIR=/mnt/hd2/data/ped-ct-seg-zip
export MYDIR_UNZIP=/mnt/hd2/data/ped-ct-seg

python ../download.py retry-2022-12-25-manifest.tcia $MYDIR

# temporarily modified below to only unzip relevant cases.
python ../unzip_retry_cases.py $MYDIR $MYDIR_UNZIP retry.yml

cd retry-cases
python ../../query.py ../retry-2022-12-25-manifest.tcia retry-cases.csv

```
