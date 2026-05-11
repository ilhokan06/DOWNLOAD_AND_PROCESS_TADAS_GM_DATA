import os
import requests
import json
import pandas as pd

# URL for the POST request
url = "https://ivmeprocessguest.afad.gov.tr/ExportData"

# Headers from your curl command
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9,tr;q=0.8,is;q=0.7,el;q=0.6",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjI2NTQ0NzcsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMCIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTAwMCJ9.c05NMwFuLO8TuUyqbYqgFf60SmxYXY7old0x9G9gKBE",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "IsGuest": "true",
    "Origin": "https://tadas.afad.gov.tr",
    "Referer": "https://tadas.afad.gov.tr/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0",
    "Username": "GuestUser",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"141\", \"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"141\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

inputloc = "G:\\My Drive\\ISTANBUL_STATIONS_SITE_EFFECTS_EVALUATION"

outputloc = "G:\\My Drive\\DOWNLOAD_TADAS_DATA_VIA_PYTHON\\STATION_BASED_DATA_DOWNLOAD"

station_list = ["3405"]

for i_stat in station_list:
    
    eq_data = pd.read_excel(inputloc+"\\"+"STATION_"+i_stat+"_EQ_REC_INFORMATION.xlsx", sheet_name="data")

    if not os.path.exists(outputloc+"\\"+i_stat):
        os.makedirs(outputloc+"\\"+i_stat)
    
    for i_eq in eq_data["EventDate"]:
        
        i_eq_arr = i_eq.split("T")[0].replace("-", "")+i_eq.split("T")[-1].replace(":", "")+"_"+i_stat

    # The data-raw part, converted to a Python dictionary
        data = {
            "filename": [i_eq_arr],
            "file_type": ["ap"],
            "file_status": "Acc",
            "export_type": "asc2",
            "user_name": "GuestUser",
            "call": "afad"
        }

        # The name of the file to save the downloaded data
        output_filename = outputloc+"\\"+i_stat+"\\"+i_eq_arr+".zip"

        try:
            # Make the POST request. The 'json' parameter automatically handles the
            # Content-Type header and JSON serialization.
            response = requests.post(url, headers=headers, json=data, stream=True)

            # Check if the request was successful
            if response.status_code == 200:
                # Save the content to a file in binary mode
                with open(output_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"File downloaded successfully to {output_filename}")
            else:
                print(f"Failed to download file. Status code: {response.status_code}")
                print(f"Response content: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

        aa = 1
