import face_module as m


base = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'#端點
key = 'a3b7cd9386e249298f9d4531d24ccdab'     #金鑰
gid = 'gp01'                                 #群組 Id
pid = '25cb65fc-3881-4ee2-9fbd-2793368d15da' #成員 Id

m.face_inint(base,key)
m.face_use(gid,' ')
#m.face_add(img)
m.face_shot('who')