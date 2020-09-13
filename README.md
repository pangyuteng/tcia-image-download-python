# tcia-image-download-python
demo python script to download images from The Cancer Imaging Archive (TCIA)


* dowload a manifest file from TCIA.

    * head to TCIA and enter your desired broad/high-level search term, for example `PET WB` 

    ```
    https://nbia.cancerimagingarchive.net/nbia-search/?text-search=%22PET%20WB%22

    ```

    *  change integer in "Show 10 entries" to a number exceeding the total search count, for example "500", if total search count is 300.

    * select all search results by selecting "shopping cart" icon in table column for each page (ideally there will only be one page, since at a prior step, we updated the count per page to exceed the total search count)

    * download manifest by clicking the `download` button.


* query more info of all series from the manifest with TCIA's REST API. The goal here is to get a final csv to actually download images of your interest. *** you will need to create your own query.py ****

    ```
    python query.py NBIA-manifest-sample.tcia download.csv
    ```

* finally, download images to your destination folder

    python download.py download.csv ${destination_folder}

