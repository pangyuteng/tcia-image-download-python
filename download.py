import sys,os
from query import TCIAClient, get_response
import pandas as pd
import traceback
import zipfile

if __name__ == '__main__':
    
    root_folder = sys.argv[1]

    df = pd.read_csv('todownload.csv')

    for n,row in df.iterrows():
        print(n,len(df))
        ct_file_path = os.path.join(root_folder,row.study_instance_uid,row.ct_series_instance_uid,'img.zip')
        pet_file_path = os.path.join(root_folder,row.study_instance_uid,row.pet_series_instance_uid,'img.zip')
        tmp_list = [
            (row.ct_series_instance_uid,ct_file_path),            
            (row.pet_series_instance_uid,pet_file_path),
        ]
        for series_instance_uid,file_path in tmp_list:

            os.makedirs(os.path.dirname(file_path),exist_ok=True)
            
            folder = os.path.dirname(file_path)
            if os.path.exists(file_path):
                if len(os.listdir(folder)) == 1:
                    try:
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(folder)
                    except:
                        traceback.print_exc()
                continue

            folder = os.path.dirname(file_path)
            basename = os.path.basename(file_path)
            if not basename.endswith('.zip'):
                basename = basename+'.zip'

            tcia_client = TCIAClient(apiKey=None, baseUrl="https://services.cancerimagingarchive.net/services/v3",resource="TCIA")
            tcia_client.get_image(seriesInstanceUid=series_instance_uid,downloadPath=folder,zipFileName=basename)

            print(len(os.listdir(folder)))
            if os.path.exists(file_path):
                if len(os.listdir(folder)) == 1:
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(folder)
                continue
