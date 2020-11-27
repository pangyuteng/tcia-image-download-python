# tcia-image-download-python
demo python script to download images from The Cancer Imaging Archive (TCIA)


## setup environment with docker

```
docker build -t tf2 .
docker run --gpus all -it -v /mnt:/mnt -v ${PWD}:/opt -w /opt -p 8888:8888 -p 6006:6006 -u $(id -u):$(id -g)  tf2 bash
```

* dowload a manifest file from TCIA.

    * head to TCIA and enter your desired broad/high-level search term, for example `PET WB` 

    ```
    https://nbia.cancerimagingarchive.net/nbia-search/?text-search=%22PET%20WB%22
    ```

    *  change integer in "Show 10 entries" to a number exceeding the total search count, for example "500", if total search count is 300.

    * select all search results by selecting "shopping cart" icon in table column for each page (ideally there will only be one page, since at a prior step, we updated the count per page to exceed the total search count)

    * download manifest by clicking the `download` button.


* (OPTIONAL) query more info of all series from the manifest with TCIA's REST API. The goal here is to get a final csv to actually download images of your interest. *** you will need to create your own `query.py` ***

    ```
    python query.py ${my_tcia_file} download.csv
    ```

* *** if you created query.py *** download images to your destination folder 

    ```
    python download.py download.csv ${dest_folder}
    python unzip_all.py ${dest_folder} ${unzipped_dest_folder} ${yaml_path}
    ```

    ```
    python download.py download.csv /mnt/hd0/data/ct-wb-zip
    python unzip_all.py /mnt/hd0/data/ct-wb-zip /mnt/hd0/data/ct-wb unzipped-ct-wb.yml
    ```
    
* *** if you skipped creating query.py *** download images to your destination folder 

    ```
    python download.py ${my_tcia_file} ${dest_folder}
    python unzip_all.py ${dest_folder} ${unzipped_dest_folder} ${yaml_path}
    ```

    ```
    mkdir -p /mnt/hd0/data/ct-lower-extremity-zip
    python download.py NBIA-manifest-sample-ct-lower-extremity.tcia /mnt/hd0/data/ct-lower-extremity-zip
    python unzip_all.py /mnt/hd0/data/ct-lower-extremity-zip /mnt/hd0/data/ct-lower-extremity unzipped-ct-lower-extremity.yml
    ```