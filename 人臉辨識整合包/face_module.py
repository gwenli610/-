import cv2
import time 
from datetime import datetime
import requests
import sqlite3

base = ''
key = ''
headers_stream = {}
headers_json = {}
headers = {}
def face_inint(b,k):
    global base, key, headers_stream, headers_json, headers
    base = b
    key = k
    headers_stream = {'Ocp-Apim-Subscription-Key': key,'Content-Type': 'application/octet-stream'}
    headers_json = {'Ocp-Apim-Subscription-Key': key,'Content-Type': 'application/json'}
    headers = {'Ocp-Apim-Subscription-Key': key}
#-----------------------------------------------------------------#
gid = ''
pid = ''
def face_use(g,p):
    global gid, pid
    gid = g
    pid = p
#-----------------------------------------------------------------#
def db_create(gpId,name,userdata):
    gp_url = base+'/persongroups/'+gpId    #創建、查詢群組的請求路線
    body = {'name': name,'userData': userdata} #請求主體的編碼
    body = str(body).encode('utf-8')
    response = requests.put(gp_url,headers=headers_json,data=body)  #發出創建請求
    if response.status_code == 200:
        print('創建群組成功')
    else:
        print('創建失敗: ', response.json())
#-----------------------------------------------------------------#
def db_check():
    headers={'Ocp-Apim-Subscription-Key':key} 
    response = requests.get(gp_url,headers=headers)#HTTP GET
    if response.status_code == 200:
        print(response.json())
    else:
        print("查詢失敗",response.json())
#-----------------------------------------------------------------#
def db_add(name,userdata):
    pson_url=f'{base}/persongroups/gp01/persons'
    body={'name':name,'userData':userdata}   #建立請求主體內容
    body=str(body).encode('utf-8')   #請求主體的編碼
    response = requests.post(pson_url,headers=headers_json,data=body)   #HTTP POST
    if response.status_code == 200:
        print('新增人員完成',response.json())
    else:
        print('新增失敗:', response.json())
#-----------------------------------------------------------------#
def face_add(img):
    img_encode = cv2.imencode('.jpg',img)[1]
    img_bytes = img_encode.tobytes()
    face_url = f'{base}/persongroups/{gid}/persons/{pid}/persistedFaces'
    response = requests.post(face_url,headers=headers_stream,data=img_bytes)
    if response.status_code == 200:
        print('新增臉部成功:',response.json())
    else:
        print('新增臉部失敗:',response.json())
#-----------------------------------------------------------------#
def face_who(img):
    faceId = face_detect(img)
    personId = face_identify(faceId)
    if personId == None:
        print('查無相符身分')
    else:
        persons = person_list(gid)
        for p in persons:
            if personId == p['personId']:
                print('歡迎:',p['name'])
                db_save('mydatabase.sqlite',p['name'])
                db_check('mydatabase.sqlite')
#-----------------------------------------------------------------#
def face_shot(job):
    isCnt=False
    face_detector=cv2.CascadeClassifier('haarcascade_frontalface_default')
    face_detector.load(r'C:/haarcascade_frontalface_default.xml')
        
    capture=cv2.VideoCapture(0)
    while capture.isOpened():
        sucess, img=capture.read()
        if not sucess:
            print('讀取影像失敗')
            continue
        img_copy = img.copy()
        faces = face_detector.detectMultiScale(img,scaleFactor=1.1,minNeighbors=5,maxSize=(200,200))
        if len(faces) ==1:
            if isCnt == False:
                t1 = time.time()
                isCnt = True
            cnter=3-int(time.time()-t1)    #秒數設定
            for(x,y,w,h) in faces:
                cv2.rectangle(img_copy,(x,y),(x+w,y+h),(0,255,255),2) #方形框
                # cv2.circle(img_copy,(int((2*x+w)/2),int((2*y+h)/2)),int((w+h)/4),(0,255,255),3) #圓形框
                cv2.putText(img_copy,str(cnter),(x+int(w/2),y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2) #倒數字
            if cnter ==0:
                isCnt = False
                filename=datetime.now().strftime('%Y-%m-%d %H.%M.%S')
                cv2.imwrite(filename+'.jpg',img)
                #-----------------------------------------------------------------#
                if job == 'add':
                    face_add(img)
                elif job == 'who':
                    face_who(img)
                #-----------------------------------------------------------------#
        else:
            isCnt = False

        cv2.imshow('Frame',img_copy)
        k = cv2.waitKey(1)
        if k == ord('q') or k==ord('Q'):
            print('exit')
            cv2.destroyAllWindows()
            capture.release()
            break
    else:
            print('開啟攝影機失敗')
#-----------------------------------------------------------------#
def face_detect(img):                   #接收影像進行臉部偵測並回傳faceId
    detect_url = f'{base}/detect?returnFaceId=true'
    img_encode = cv2.imencode('.jpg', img)[1]
    img_bytes = img_encode.tobytes()
    response = requests.post(detect_url,headers=headers_stream,data=img_bytes)
    if response.status_code == 200:
        face = response.json()
        if not face:
            print("照片中沒有偵測到人臉")
        else:
            faceId = face[0]['faceId']
            return faceId
#-----------------------------------------------------------------#
def face_identify(faceId):              #進行身分識別
    idy_url = f'{base}/identify'
    body = str({'personGroupId':gid,'faceIds': [faceId]})
    response = requests.post(idy_url,headers=headers_json,data=body)
    if response.status_code == 200:
        person = response.json()
        if not person[0]['candidates']:
            return None
        else:
            personId = person[0]['candidates'][0]['personId']
            print(personId)
            return personId
#-----------------------------------------------------------------#
def person_list(gid):
    pson_url=f'{base}/persongroups/gp01/persons'
    response = requests.get(pson_url,headers=headers)
    if response.status_code == 200:
        print('查詢人員完成')
        return response.json()
    else:
        print("查詢人員失敗", response.json())
#-----------------------------------------------------------------#        
def db_save(db,name):
    connect = sqlite3.connect(db)
    sql = 'create table if not exists mytable ("姓名" TEXT, "打卡時間" TEXT)'
    connect.execute(sql)
    save_time=str(datetime.now().strftime('%Y-%m-%d %H%M%S'))

    sql = f'insert into mytable values("{name}", "{save_time}")'
    connect.execute(sql)
    connect.commit()
    connect.close()
    print('儲存成功')
#-----------------------------------------------------------------#
def db_check(db):
    try:
        connect= sqlite3.connect(db)
        sql= 'select * from mytable'
        cursor=connect.execute(sql)
        dataset=cursor.fetchall()
        print('姓名\t打卡時間')
        print('----\t ----')
        for data in dataset:
            print(f"{data[0]}\t{data[1]}")
    except:
        print('讀取資料庫錯誤')
    connect.close()
        