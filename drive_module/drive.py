import os, json
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
import io
load_dotenv()

CREDENTIALS = json.loads(os.environ.get('CREDENTIALS'))

if os.path.exists('credentials.json'):
    pass
else:
    with open('credentials.json', 'w') as credFile:
        json.dump(CREDENTIALS, credFile)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'

service = build('drive', 'v3')


# FOLDER ID MAP FOR DEPARTMENT AND YEAR 
dep_id_map = {
    'CS': {'__id__': '1rPEdBTFcxpJiJ0Ik8RVxMBXLy1U4tWh9', 'FE': '1LTfI4IFIh50oKQb5j4moxetl0hh3hX06', 'SE': '1O6w2ZbVRpV7oH_c7gELQDFK3YgWNu9nS', 'TE': '1I1s-ROgtxhbwMCsrRD5p6mJEoBYsIvV5', 'BE': '11iM5oOtTkxE-UO3eWvJlntYAC1az5xgV'}, 
    'IT': {'__id__': '1oEPyC7gtjq_aBsyGi-cjZ0bgZafuv78F', 'FE': '15MinIe6bofCfaGdfvTTUPoSCQpzKBnBn', 'SE': '1CP-rna2yqvqCFx6dRcVkmwRF2FLppuAz', 'TE': '19pGmnrby8a0tfRrbkE_r-b2SiEctcEXk', 'BE': '1ONnvNiDtChE5O8LH47nYYdAmZ8VvKtvL'},
    'Elex': {'__id__': '1J_30yCWu1CHyxXQd5Igux89tdMTp5LQC', 'FE': '1bfM7_ELZzFCyS9zVSL5gcFvRlQHveEx8', 'SE': '1vpdZy9OMgyqsHsmNqwbTvuSGzNej_Xd5', 'TE': '15wEAHFxCohRZnjnbd1C1EwNAwgiMiwaB', 'BE': '1BuMw3TH9FLDYo9QYQ658IxTP4__dl9Vu'}, 
    'EXTC': {'__id__': '1i71UTQWO9Qd1zPWihvweE8zJB2-tLEuU', 'FE': '1YtZ9hfJW3GUloBhdzEA2_48xX8hQtIeP', 'SE': '1bsJdTubGvacTf3T8AqESUWmibM_Gw4qt', 'TE': '13YHnT4KmlTb96LF1meZq1FgBGL8Ipvxz', 'BE': '1m5dCqaSr7ubxa-pac2d9NPBRDShRDpFk'}, 
    'Chemical': {'__id__': '158DxFfNqnH5R5RcRhz8mLtde1h2Q3Ruq', 'FE': '1T1g0ld9qSxYHV3WEovjy2n5kFH9HhQRY', 'SE': '1-QxBfxJ67yjt0IcaiLUSKDXk4prdJ5JR', 'TE': '1iP_8U8iKbZ32Z1GYBqqHt6FoC1Aj7TXE', 'BE': '11BvxOX-nDAx8Q_Ak9VedIiSCVk2Qhvaj'}, 
    'Production': {'__id__': '1rh_yHZPaHC1S-BtBfB0nHyoUpH-XdSjR', 'FE': '1KaBWaiQazOsO5EBDTohO7w0qREIXQwzy', 'SE': '1GRmh-WQ8kVxuYupBv15X2AN3tlj-R-GC', 'TE': '1Q1wqTGKVQcKVoNSi4fHvu2TAH3XeC3Q2', 'BE': '1UBUoUHkmdTTJhcxJ_7gPeNO8sH8LwEBw'}, 
    'Mechanical': {'__id__': '1mu9p_pb-MYZTYHFaUk3TvNNJTuNJs6wo', 'FE': '12Zv6Gk3Pmscd24GCf3JIZXjKfJOFv2YU', 'SE': '1-hk8lwrp6EC-9Zx9I2epQPEm1UxYr1Z4', 'TE': '19LS0ehG4hAiX8ZIR-oH0Avv8Dk8g0ttn', 'BE': '1lfyNULy1qp1wSPrAZbWYy9iW86p2_XIP'}, 
    'Biomedical': {'__id__': '1Zg8toX8GK3p_Z1SymPVprKbF2F_U2YU7', 'FE': '1YfW6Tbcp9xdrqvjkf8n2B5QsnvEyuFt0', 'SE': '1F1WIfuYFwY5Yt1AEuZ5WsCm0hZ--hMK_', 'TE': '1X4PJ4C40wtK429dUVMQAHM53U-QEDav2', 'BE': '1NYAeveAuTHxPfM7DiRhSyO7Ju8gYs_NJ'}, 
    'Data Science': {'__id__': '1MTwGa7Pl0tJeWztj-I6qMmTdbiKPE8l7', 'FE': '1VwYrbMJSBhVWgD8wZAeDSeh2kQqZxMCe', 'SE': '177kvavqIz1-jWzPqZvVpK9sTVfCdX0b_', 'TE': '1FvGUNRwBOxgw-d2S1TXtZGDNoKe-y2Oc', 'BE': '1GRClp_r0ClNfKHs2lTBFlI6k6W9Lc8cp'}, 
    'Ai-ML': {'__id__': '1go0JLO7Nst_xy1ZgQovFaTY_8XRDPjxn', 'FE': '1V2dSl_GmoyziYOPPI_3Zc85lfkr0R_t0', 'SE': '1W9MNd_0iOEShxQ-0lOYRwDgXEilAau82', 'TE': '1DEgZQiboWCj9dQclwProvwzWQ0s70FNO', 'BE': '1sDWpNx-cFx9a_VMCnW4AxFMKWQzO37TH'}, 
    'AI-DS': {'__id__': '19wsdhGojYxXHQMEoCCcl4Y0UEIL3siV9', 'FE': '1Q6iuNZvnUjkPDGr01vIGsRHXyxLW9Mqo', 'SE': '1TOZexBjqEGbqREywfAA2OmWgdFYtHxIa', 'TE': '1eGe20SZF3WVc0COl9YKbkaT6F85RVwfG', 'BE': '1Tcag0NgLxfas_22EKeD0kBwBPDe0YV0x'}, 
    'IOT and Cyber Security with Blockchain': {'__id__': '1m-A7qVYoY7RcZtVEDCkkN4xWamPm5RSb', 'FE': '16jNE9b56YRtu9luZFLA5W6bF62kyD50d', 'SE': '15_pw9mchO2fRdsFdvjUhI9d4wEXCyChy', 'TE': '15zcyXFdv9Bz2aieNm_6G6CCpooulu8-P', 'BE': '1SYW8ETtAux5JQ1Xl96LYOsL6l4d4tnvC'}
}

#function to add folder to drive
def add_folder(name, dep, year):
    parent_folder_id = dep_id_map[dep][year]
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }

    s = service.files().create(body=file_metadata).execute()
    return s

#function to add pdf file to drive
def add_file(file, parent_folder_id, sap):
    mime_types = ["image/jpeg"]
    
    file_metadata = {
        'name' : file,
        'parents' : [parent_folder_id]
    }
    media = MediaFileUpload('{0}'.format(file), mimetype=mime_types[0])
    service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    os.remove(str(sap)+".jpg")