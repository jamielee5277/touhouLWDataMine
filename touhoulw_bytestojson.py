import os
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import unpad
from binascii import b2a_hex, a2b_hex
import msgpack#plz use 0.6.2 ,1.0.0 will fail!
import json

#place the script in folder contains *.bytes
key=a2b_hex("06C2A032C28C28C29F02C29B26C29F11")
for name in os.listdir():
    if not name.endswith(".bytes"):
        continue
    f=open(name,'rb')
    iv=f.read(16)
    crypto=AES.new(key, AES.MODE_CBC, iv)
    data=f.read()
    f.close()
    plain=unpad(crypto.decrypt(data),16)
    j=json.dumps(msgpack.unpackb(plain,use_list=False, raw=False),ensure_ascii=False,indent=1)
    #print(j)
    f=open(name.replace(".bytes",".json"),"wb")
    f.write(bytes(j,encoding='utf-8'))
    f.close()
    