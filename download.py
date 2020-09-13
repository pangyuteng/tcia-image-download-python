import sys,os
from query import TCIAClient, get_response
import pandas as pd
import traceback
import zipfile

if __name__ == '__main__':
    
    csv_file_path = sys.argv[1]
    root_folder = sys.argv[2]

    df = pd.read_csv(csv_file_path)

    for n,row in df.iterrows():
        print(n,len(df))
        study_instance_uid = row.study_instance_uid
        series_instance_uid = row.series_instance_uid
        file_path = os.path.join(root_folder,study_instance_uid,series_instance_uid,'img.zip')
        
        if os.path.exists(file_path):
            continue
            
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        
        folder = os.path.dirname(file_path)
        basename = os.path.basename(file_path)

        tcia_client = TCIAClient(apiKey=None, baseUrl="https://services.cancerimagingarchive.net/services/v3",resource="TCIA")
        tcia_client.get_image(seriesInstanceUid=series_instance_uid,downloadPath=folder,zipFileName=basename)

