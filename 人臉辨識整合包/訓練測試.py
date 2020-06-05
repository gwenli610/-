ㄣimport requests
import cv2

def pratice():
    response = requests.post(train_urlp,headers=headers)  
    if response.status_code == 202:
        print("開始訓練...")
    else:
        print("訓練失敗",response.json())
        
def checkasult():
    response = requests.get(train_urlg,headers=headers)
    if response.status_code == 200:
        print("訓練結果:",response.json())
    else:
        print("查看失敗",response.json())


base = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'#端點
key = 'a3b7cd9386e249298f9d4531d24ccdab'     #金鑰
gId = 'gp01'
train_urlp = f'{base}/persongroups/{gId}/train'
train_urlg = f'{base}/persongroups/{gId}/training'
headers = {'Ocp-Apim-Subscription-Key': key}
k='p'
while(k == 'P' or k == 'p' or k == 'C' or k == 'c'):
    k=input("訓練請輸入 P 查看結果請輸入 C:") 
    if k == 'P' or k == 'p':
        pratice()
    elif  k == 'C' or k == 'c':
        checkasult()
