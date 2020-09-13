import os
import sys
import ast
import traceback
import datetime
import numpy as np
import pandas as pd
from tciaclient import TCIAClient
import urllib3, urllib,sys
import concurrent.futures

def get_response(response):
    if response.status == 200:
        return response.data.decode('utf-8')
    else:
        raise ValueError("Error: " + str(response.status))
    
if __name__ == '__main__':
    
    manifest_file_path = sys.argv[1]
    csv_file_path = sys.argv[2]
  
    with open(manifest_file_path,'r') as f:
        content = [x for x in f.read().split('\n') if len(x) > 0]

    i = content.index('ListOfSeriesToDownload=')
    series_instance_uid_list = content[i+1:]

    maxsize = 3
    
    study_data = []
    series_data = []
    tcia_client = TCIAClient(apiKey=None, baseUrl="https://services.cancerimagingarchive.net/services/v3",resource = "TCIA",maxsize=maxsize)
    
    if os.path.exists('data_series.csv'):
        df_series = pd.read_csv('data_series.csv')
    else:
        with concurrent.futures.ThreadPoolExecutor(maxsize) as executor:
            myfutures = {executor.submit(tcia_client.get_series, seriesInstanceUID=x):x for x in series_instance_uid_list}
            for future in concurrent.futures.as_completed(myfutures):
                try:                    
                    response = future.result()
                    r = get_response(response)
                    info_dict = ast.literal_eval(r)[0]
                    series_data.append(info_dict)
                    print(datetime.datetime.now(),'series')
                except:
                    traceback.print_exc()

        df_series = pd.DataFrame(series_data)
        df_series.to_csv('data_series.csv',index=False)

    study_instance_uid_list = np.unique(df_series.StudyInstanceUID.values)

    if os.path.exists('data_study.csv'):
        df_study = pd.read_csv('data_study.csv')
    else:
        with concurrent.futures.ThreadPoolExecutor(maxsize) as executor:
            myfutures = {executor.submit(tcia_client.get_patient_study, studyInstanceUid=x):x for x in study_instance_uid_list}
            for future in concurrent.futures.as_completed(myfutures):
                try:
                    print('study')
                    response = future.result()
                    r = get_response(response)
                    info_dict = ast.literal_eval(r)[0]
                    study_data.append(info_dict)
                    print(datetime.datetime.now(),'study')
                except:
                    traceback.print_exc()

        df_study = pd.DataFrame(study_data)
        df_study.to_csv('data_study.csv',index=False)

    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
    else:
        df = df_series.merge(df_study,
            left_on=['StudyInstanceUID','Collection'], 
            right_on = ['StudyInstanceUID','Collection'], how='left')
        df.to_csv('data.csv',index=False)

    #
    # df.columns
    #
    # SeriesInstanceUID,StudyInstanceUID,Modality,ProtocolName,SeriesDate,SeriesDescription,
    # BodyPartExamined,SeriesNumber,Collection,Manufacturer,ManufacturerModelName,
    # SoftwareVersions,Visibility,ImageCount,PatientID,PatientName,PatientSex,StudyDate,
    # StudyDescription,PatientAge,SeriesCount
    #

    # get unique patient - study - pet/ct pair, get one with large image count, early study date.
    data = {}
    count=0
    for PatientID in np.unique(df.PatientID):

        tmpP = df[df['PatientID']==PatientID]
        
        if PatientID not in data.keys():
            data[PatientID]=[]

        for StudyInstanceUID in np.unique(tmpP.StudyInstanceUID):

            tmpS = df[df['StudyInstanceUID']==StudyInstanceUID]
            
            pet_list = []
            ct_list = []
            # find pet corrected
            tmpPET = tmpS[tmpS['Modality']=='PT']
            for n,row in tmpPET.iterrows():
                if 'nac' in row.SeriesDescription.lower():
                    continue
                if 'uncorrected' in row.SeriesDescription.lower():
                    continue
                if 'cor' in row.SeriesDescription.lower():
                    continue
                if 'sag' in row.SeriesDescription.lower():
                    continue
                if 'mip' in row.SeriesDescription.lower():
                    continue
                if 'PET WB' in row.SeriesDescription:
                    pet_list.append(row)

            if len(pet_list) == 0:
                continue
            if len(pet_list) != 1:
                print(len(pet_list),[x.SeriesDescription for x in pet_list])
                continue

            # find pet corrected
            tmpCT = tmpS[tmpS['Modality']=='CT']
            for n,row in tmpCT.iterrows():
                if 'cor' in row.SeriesDescription.lower():
                    continue
                if 'sag' in row.SeriesDescription.lower():
                    continue
                if 'mip' in row.SeriesDescription.lower():
                    continue
                if 'scout' in row.SeriesDescription.lower():
                    continue
                if 'topogram' in row.SeriesDescription.lower():
                    continue
                ct_list.append(row)

            if len(pet_list) != 1 or len(ct_list) != 1:
                continue
            
    # SeriesInstanceUID,StudyInstanceUID,Modality,ProtocolName,SeriesDate,SeriesDescription,
    # BodyPartExamined,SeriesNumber,Collection,Manufacturer,ManufacturerModelName,
    # SoftwareVersions,Visibility,ImageCount,PatientID,PatientName,PatientSex,StudyDate,
    # StudyDescription,PatientAge,SeriesCount

    # Collection,PatientID,PatientName,PatientSex,StudyInstanceUID,StudyDate,
    # StudyDescription,PatientAge,SeriesCount

            item = dict(
                collection = pet_list[0].Collection,
                patient_id = PatientID,
                patient_sex = pet_list[0].PatientSex,
                patient_age = pet_list[0].PatientAge,
                study_instance_uid = StudyInstanceUID,
                study_date = ct_list[0].StudyDate,
                study_description = pet_list[0].StudyDescription,
                pet_series_description = pet_list[0].SeriesDescription,
                pet_img_count = pet_list[0].ImageCount,
                pet_series_instance_uid = pet_list[0].SeriesInstanceUID,
                ct_series_description = ct_list[0].SeriesDescription,
                ct_img_count = ct_list[0].ImageCount,
                ct_series_instance_uid = ct_list[0].SeriesInstanceUID,
                series_instance_uid = ct_list[0].SeriesInstanceUID,
            )

            data[PatientID].append(item)

    count = 0
    mylist = []
    for k,v in data.items():
        if len(v) == 0:
            continue
        count+=1
        if len(v) > 0:
            v = sorted(v,key=lambda x: x['study_date'])
            mylist.append(v[0])
        else:
            mylist.append(v[0])

    pd.DataFrame(mylist).to_csv(csv_file_path,index=False)
    print(count)