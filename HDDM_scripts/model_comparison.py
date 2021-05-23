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


# Transform into data frame and store in dic.csv
vformula = []
aformula = []
tformula = []
zformula = []
nsamples = []
dic = []
bdic = []
 

# Load and concatenate models and extract DIC information
for x in os.listdir(path):


    models = [];

    modelname = x.split('_')[0]
    nsamples.append(x.split('_')[-1])

    modelformula = x.split('_')[0]
    if len(modelformula.split('z')) == 2:

        zformula.append(modelformula.split('z')[-1])
        modelformula = modelformula.split('z')[0]
    else:
        zformula.append(None)
    
    if len(modelformula.split('t')) == 2:

        tformula.append(modelformula.split('t')[-1])
        modelformula = modelformula.split('t')[0]
    else:
        tformula.append(None)

    if len(modelformula.split('a')) == 2:

        aformula.append(modelformula.split('a')[-1])
        modelformula = modelformula.split('a')[0]
    else:
        aformula.append(None)

    if len(modelformula.split('v')) == 2:

        vformula.append(modelformula.split('v')[-1])
        modelformula = modelformula.split('v')[0]
    else:
        vformula.append(None)

    for i in range(5):
        m = hddm.load(path + x + '/' + x + '_' + str(i))
        models.append(m)
    m_comb = concat_models(models)
    print(modelname)
    print("****DIC: %f" %m_comb.dic)
    print("****BPIC: %f" %(m_comb.dic_info['pD'] + m_comb.dic))
    
    dic_dict[modelname] = m_comb.dic
    bdic_dict[modelname] = m_comb.dic_info['pD'] + m_comb.dic

    dic.append(m_comb.dic)
    bdic.append(m_comb.dic_info['pD'] + m_comb.dic)


# Transform into data frame and store in dic.csv
"""
vformula = []
aformula = []
tformula = []
zformula = []
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
"""


df = pd.DataFrame({'v':vformula,
                   'a':aformula,
                   't':tformula,
                   'z':zformula,
                   'nsamples':nsamples,
                   'DIC':dic,
                   'BDIC':bdic})


df.to_csv('dic.csv',index=False)