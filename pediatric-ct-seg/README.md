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



```

