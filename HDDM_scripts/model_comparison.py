import hddm
import sys
from kabuki.utils import concat_models
import numpy as np
import pandas as pd
import os


# When running the script, feed the path of output to the program
# The path should end with '/'
path = sys.argv[1]

dic_dict = {}
bdic_dict = {}


# Load and concatenate models and extract DIC information
for x in os.listdir(path):
    modelname = x.split('_')[0]
    models = []
    for i in range(5):
        m = hddm.load(path + x + '/' + x + '_' + str(i))
        models.append(m)
    m_comb = concat_models(models)
    print(modelname)
    print("****DIC: %f" %m_comb.dic)
    print("****BPIC: %f" %(m_comb.dic_info['pD'] + m_comb.dic))
    
    dic_dict[modelname] = m_comb.dic
    bdic_dict[modelname] = m_comb.dic_info['pD'] + m_comb.dic


# Transform into data frame and store in dic.csv
vformula = []
aformula = []
tformula = []
dic = []
bdic = []

formulas = ['C','RC','PC','RPC']

for vp in formulas:
    for ap in formulas:
        vformula.append('+'.join(vp))
        aformula.append('+'.join(ap))
        tformula.append(None)
        dic.append(dic_dict['v'+vp+'a'+ap])
        bdic.append(bdic_dict['v'+vp+'a'+ap])
        
for tp in formulas:
    vformula.append('+'.join('RPC'))
    aformula.append('+'.join('RPC'))
    tformula.append('+'.join(tp))
    dic.append(dic_dict['vRPCaRPC'+'t'+tp])
    bdic.append(bdic_dict['vRPCaRPC'+'t'+tp])


df = pd.DataFrame({'v':vformula,
                   'a':aformula,
                   't':tformula,
                   'DIC':dic,
                   'BDIC':bdic})


df.to_csv('dic.csv',index=False)