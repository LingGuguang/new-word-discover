from Delete import Delete
import pandas as pd
import jieba
import re

# #以下为弹幕去重
txt = 'danmu.txt'
save_txt = 'save.txt'
ammos = []

with open(txt, 'r', encoding='utf-8') as t:
    for ammo in t.readlines():
        ammos.append(ammo[:-1])
#print(len(ammos)) = (48000)

dele = Delete(ammos)
ammos = dele.delete()

ammos = [re.sub(r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+", " ", ammo) 
            for ammo in ammos]
    
ammos = [ammo.replace(' ','') for ammo in ammos]

with open(save_txt, 'w', encoding='utf-8') as f:
    for ammo in ammos:
        if(len(ammo)>2):
            f.write(ammo + '\n')
