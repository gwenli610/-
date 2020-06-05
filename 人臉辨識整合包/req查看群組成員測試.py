import requests
import cv2
base = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'#端點
key = 'a3b7cd9386e249298f9d4531d24ccdab' #金鑰
headers = {'Ocp-Apim-Subscription-Key': key}

def person_list(gid):
    pson_url=f'{base}/persongroups/gp01/persons'
    response = requests.get(pson_url,headers=headers)
    if response.status_code == 200:
        print('查詢人員完成')
        return response.json()
    else:
        print("查詢人員失敗", response.json())

persons=person_list('gp01')
print(persons)

