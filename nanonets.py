import requests
import json

def use_nanonets_model_on_pdf(filepath):
    url = 'https://app.nanonets.com/api/v2/OCR/Model/fa93fda1-cbdd-4860-b72f-00c93c8d5c9f/LabelFile/'
    data = {'file': open(filepath, 'rb')}
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('hQ4sisU1scoI69E9Tt5-AW1MgCMuoitn', ''), files=data)
    #print(type(response))

    # Note: <class 'requests.models.Response'> has json() methods to deserializes.
    with open("data_file.json", "w") as write_file:
        json.dump(response.json(), write_file)

use_nanonets_model_on_pdf('01 Lõnseddel 14.12.2020-17.01.2021.PDF')

with open("data_file.json", "r") as read_file:
    data = json.load(read_file)
    #print(type(data['result']))

    for item in data['result']:
        #print(item['prediction'])

        for value in item['prediction']:
            print(value['label'])

            if value['label'] == "periode":
                print(value['ocr_text'])

            if value['label'] == "timetal":
                print(value['ocr_text'])

            if value['label'] == "udbetalt":
                print(value['ocr_text'])


    if "periode" in data:
        salary_periode = prediction[0]
        print(salary_periode)
