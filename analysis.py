import re 
import numpy 
import pandas as pd

save = 'save.txt'
ammos = pd.read_csv(save, encoding='utf-8', header=None)

'''
1、2 都可以拆成1-gram，即单字词
'''
#1
ammos = [list(ammo) for ammo in ammos[0]]
#2
# ammos = list(map(lambda ammo: list(ammo), ammos[0]))



