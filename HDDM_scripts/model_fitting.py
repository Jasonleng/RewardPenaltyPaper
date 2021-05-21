
"""
Script for model fitting
Command line inputs:

1: Study: Study1 or Study2
2: Is random errors included in the data: 0 = No, 1 = Yes
3 - 6: Formula coding for v, a, t, z
    each input is 3-digits, for example, '001'
    0: Not included, 1: Included

    1st digit -> reward
    2nd digit -> penalty
    3rd digit -> congruence

7: Is starting point bias included: 0 = No, 1 = Yes
8: Number of total samples from MCMC
9: Number of burned sample from MCMC

Output files will be stored in ../output/

Author:
    Xiamin Leng, May 2021, xiamin_leng@brown.edu
"""


import matplotlib
matplotlib.use('agg')
import hddm
import pandas as pd
import matplotlib.pyplot as plt
from kabuki.analyze import gelman_rubin
from kabuki.utils import concat_models
import sys
import os
import multiprocessing


sys.setrecursionlimit(10000000)


def savePatch(self, fname):
    import pickle
    with open(fname, 'wb') as f:
        pickle.dump(self, f)

study = sys.argv[1]
isRandomIncluded = int(sys.argv[2])==1
vFormula = sys.argv[3]
aFormula = sys.argv[4]
tFormula = sys.argv[5]
zFormula = sys.argv[6]
includeBias = int(sys.argv[7])==1
nSample = int(sys.argv[8])
nBurned = int(sys.argv[9])

if isRandomIncluded:
    datafile = 'hddm_data_all_errors.csv'
else:
    datafile = 'hddm_data_ae_only.csv'

df = pd.read_csv('../data/' + study + '/' + datafile,low_memory=False)
data = hddm.utils.flip_errors(df)

print(datafile)

if study == 'Study1':
    data['catPunLevel'] = data['catPunLevel'].astype('category').cat.reorder_categories(['High Penalty','Low Penalty'])
    data['catRewLevel'] = data['catRewLevel'].astype('category').cat.reorder_categories(['High Reward','Low Reward'])
elif study == 'Study2':
    data['catPunLevel'] = data['catPunLevel'].astype('category').cat.reorder_categories(['Low Penalty', 'Medium Penalty','High Penalty'])
    data['catRewLevel'] = data['catRewLevel'].astype('category').cat.reorder_categories(['Low Reward', 'Medium Reward','High Reward'])
else:
    sys.exit("Study does not match")

hddm.HDDM.savePatch = savePatch
modelDict = {'v':vFormula,'a':aFormula,'t':tFormula,'z':zFormula}
if study == 'Study1':
    addList = ['+C(catRewLevel,Sum)','+C(catPunLevel,Sum)','+C(catCong,Sum)']
    mulList = ['*C(catRewLevel,Sum)','*C(catPunLevel,Sum)','*C(catCong,Sum)']
if study == 'Study2':
    addList = ['+C(catRewLevel,Poly)','+C(catPunLevel,Poly)','+C(catCong,Sum)']
    mulList = ['*C(catRewLevel,Poly)','*C(catPunLevel,Poly)','*C(catCong,Sum)']

argList = ['R','P','C']
modelList = []
modelName = ''

for dv in ['v','a','t','z']:

    modelString = modelDict[dv]
    modelEquation = ''
    modelNamePart = ''

    if modelString == '000':
        continue
    else:

        for i in range(3):
            if modelString[i] == '1':
                modelEquation = modelEquation + addList[i]
                modelNamePart = modelNamePart + argList[i]
            if modelString[i] == '2':
                modelEquation = modelEquation + mulList[i]
                modelNamePart = modelNamePart + '_' + argList[i]

        modelEquation = dv + '~' + modelEquation[1:]
        modelNamePart = dv + modelNamePart
    modelList.append(modelEquation)
    modelName = modelName + modelNamePart


modelName = modelName + '_' + study + '_' + sys.argv[2] + '_' + sys.argv[8]
print(modelList)
print(modelName)

if isRandomIncluded:
    outputPath = '../output/' + study + '/all_errors/' + modelName
else:
    outputPath = '../output/' + study + '/ae_only/' + modelName

if not os.path.exists(outputPath):
    os.makedirs(outputPath)

def run_model(id):

    m = hddm.HDDMRegressor(data, modelList,bias=includeBias,
        include='p_outlier',group_only_regressors = False)

    m.find_starting_values()
    m.sample(nSample, burn=nBurned, dbname=outputPath + '/' + modelName+'_'+str(id)+'.db', db='pickle')
    m.savePatch(outputPath + '/' +modelName+'_'+str(id))
    return m


pool = multiprocessing.Pool()
models = pool.map(run_model, range(5))
pool.close()

m_rhat = gelman_rubin(models)
pd.DataFrame.from_dict(m_rhat, orient='index').to_csv(outputPath + '/'+modelName+'_RHat.csv')

m_comb = concat_models(models)
m_comb_export = m_comb.get_traces()
m_comb_export.to_csv(outputPath + '/' + modelName+'_traces.csv')
print("DIC: %f" %m_comb.dic)

results = m_comb.get_traces()
results.to_csv(outputPath + '/' + modelName+'_Results.csv')
summary = m_comb.gen_stats()
summary.to_csv(outputPath + '/' + modelName+'_Summary.csv')
