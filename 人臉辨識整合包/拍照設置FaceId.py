import face_module as m


base = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'#端點
key = 'a3b7cd9386e249298f9d4531d24ccdab'     #金鑰
gid = 'gp01'                                 #群組 Id
pid = '2088659c-8271-4c59-a6eb-1428607b5bf0' #成員 Id  改為步驟2取得的personId

m.face_inint(base,key)
m.face_use(gid,pid)
m.face_shot('add')