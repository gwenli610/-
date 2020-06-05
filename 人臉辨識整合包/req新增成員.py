import requests
base = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'#端點
key = 'a3b7cd9386e249298f9d4531d24ccdab'   #金鑰


pson_url=f'{base}/persongroups/gp01/persons'
headers_json = {'Ocp-Apim-Subscription-Key': key,'Content-Type': 'application/json'}
body={'name':'蔡禧','userData':'小帥哥'}   #建立請求主體內容  修改處!!!
body=str(body).encode('utf-8')   #請求主體的編碼
response = requests.post(pson_url,headers=headers_json,data=body)   #HTTP POST
if response.status_code == 200:
    print('新增人員完成',response.json())
else:
    print('新增失敗:', response.json())