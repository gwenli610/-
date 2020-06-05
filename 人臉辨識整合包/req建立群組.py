import requests

def db_create():
    response = requests.put(gp_url,headers=headers_json,data=body)  #發出創建請求
    if response.status_code == 200:
        print('創建群組成功')
    else:
        print('創建失敗: ', response.json())
def db_check():
    response = requests.get(gp_url,headers=headers)#HTTP GET
    if response.status_code == 200:
        print(response.json())
    else:
        print("查詢失敗",response.json())
def db_add():
    response = requests.post(pson_url,headers=headers_json,data=body1)   #HTTP POST
    if response.status_code == 200:
        print('新增人員完成',response.json())
    else:
        print('新增失敗:', response.json())

base = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'#端點
#--------------------------------------------------------------------------#創建
gp_url = base+'/persongroups/gp01'    #創建、查詢群組的請求路線
key = 'a3b7cd9386e249298f9d4531d24ccdab'   #金鑰
headers_json = {'Ocp-Apim-Subscription-Key': key,'Content-Type': 'application/json'}
body = {'name': '旗標科技公司','userData': '位於台北市'} #請求主體的編碼
body = str(body).encode('utf-8')
#--------------------------------------------------------------------------#請求
headers={'Ocp-Apim-Subscription-Key':key}   #請求標頭

#--------------------------------------------------------------------------#新增成員
pson_url=f'{base}/persongroups/gp01/persons'
body1={'name':'周永','userData':'苗栗人'}   #建立請求主體內容
body1=str(body1).encode('utf-8')   #請求主體的編碼




# db_create()
# db_check()
db_add()
