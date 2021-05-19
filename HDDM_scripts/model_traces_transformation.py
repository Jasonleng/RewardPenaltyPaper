"""
Script for transforming traces and inferring reward/penalty weights

Author:
	Xiamin Leng, May 2021, xiamin_leng@brown.edu
"""

import hddm
import pandas as pd
import numpy as np
import sympy

traces = pd.read_csv(sys.argv[1])

nSubj = 32 # Number of subjects in the data


# Placeholder for group level summary
traces_summary_group = {'Cond':[],
                        'v':[],
                        'a':[],
                        'v_sd':[],
                        'a_sd':[]}

# Placeholder for subject level summary
traces_summary_sub = {'subj':[],
                      'Cond':[],
                      'v':[],
                      'a':[],
                      't':[]}

# Weights for conditions, used to transfer contrast into levels
# DOUBLE CHECK THIS PART BEFORE MOVING FORWARD!!!
weights = {'RHPH':(1,1),
           'RHPL':(1,-1),
           'RLPH':(-1,1),
           'RLPL':(-1,-1)}


# Generate group level summary
for name,value in weights.items():
    traces_summary_group['Cond'].append(name)
    for parameter,intercept in [('v','v_Intercept'),('a','a_Intercept')]:
        # Get the group level estimate of reward effect
        colname_rew = parameter + '_C(catRewLevel, Sum)[S.High Reward]'
        # Get the group level estimate of penalty effect
        colname_pun = parameter + '_C(catPunLevel, Sum)[S.High Penalty]'
        
        # Calculate the trace of parameter under specific condition 
        # from parameter estimate and weights
        trace = traces[intercept] + value[0] *\
        traces[colname_rew] + value[1] * traces[colname_pun]
        # Transform threshold
        if parameter == 'a':
            trace = trace/2
        traces_summary_group[parameter].append(np.mean(trace))
        traces_summary_group[parameter+'_sd'].append(np.std(trace))

# Generate subject level summary
for subj in range(1,nSubj+1):
    for name,value in weights.items():
        traces_summary_sub['subj'].append(subj)
        traces_summary_sub['Cond'].append(name)
        # Store the subject-specific ndt
        traces_summary_sub['t'].append(np.mean(traces['t_subj.'+str(subj)]))
        for parameter,intercept in [('v','v_Intercept'),('a','a_Intercept')]:
            # Get the subject level estimate of intercept
            colname_int = intercept + '_subj.' + str(subj)
            # Get the subject level estimate of reward effect
            colname_rew = parameter + '_C(catRewLevel, Sum)[S.High Reward]' +\
            '_subj.' + str(subj)
            # Get the subject level estimate of penalty effect
            colname_pun = parameter + '_C(catPunLevel, Sum)[S.High Penalty]' +\
            '_subj.' + str(subj)
            # Calculate the trace of subject-specifc parameter under 
            # specific condition from parameter estimate and weights
            trace = traces[colname_int] + value[0] *\
            traces[colname_rew] + value[1] * traces[colname_pun]
            # Transform threshold
            if parameter == 'a':
                trace = trace/2
            traces_summary_sub[parameter].append(np.mean(trace))


# Generate symbolic formula for the inference of R and P
a = sympy.Symbol('a')
v = sympy.Symbol('v')
r = sympy.Symbol('r')
p = sympy.Symbol('p')
ndt = sympy.Symbol('ndt')

DT = a/v*sympy.tanh(a*v)
ER = 1/(1 + sympy.exp(2*a*v))
cost = v * v
rr = (r * (1 - ER) - p * ER)/(ndt + DT) - cost

C_R = (1 - ER)/(DT + ndt)
C_P = -ER/(DT+ndt)
C_R_da = sympy.diff(C_R,a)
C_R_dv = sympy.diff(C_R,v)
C_P_da = sympy.diff(C_P,a)
C_P_dv = sympy.diff(C_P,v)

cost_da = sympy.diff(cost,a)
cost_dv = sympy.diff(cost,v)

C = C_R_dv * C_P_da - C_P_dv * C_R_da
R = (C_P_da * cost_dv - C_P_dv * cost_da)/C
P = (-C_R_da * cost_dv + C_R_dv * cost_da)/C
RR = C_R * R + C_P * P - cost

RR_da2 = sympy.diff(C_R,a,a)*R + sympy.diff(C_P,a,a)*P-sympy.diff(cost,a,a)
RR_dv2 = sympy.diff(C_R,v,v)*R + sympy.diff(C_P,v,v)*P-sympy.diff(cost,v,v)
RR_dadv = sympy.diff(C_R,a,v)*R + sympy.diff(C_P,a,v)*P-sympy.diff(cost,a,v)

mask = sympy.logic.boolalg.And((RR_dv2*RR_da2-RR_dadv*RR_dadv)>0,RR_da2<0)

# Transfer symbolic equation to python function
f_R = sympy.lambdify([a,v,ndt],R)
f_P = sympy.lambdify([a,v,ndt],P)
f_RR = sympy.lambdify([a,v,ndt],RR)
f_mask = sympy.lambdify([a,v,ndt],mask)


# Calculate R and P based on subject level DDM parameters in each condition and mean NDT
P = f_P(np.array(traces_summary_sub['a']),np.array(traces_summary_sub['v']),np.mean(traces['t']))
R = f_R(np.array(traces_summary_sub['a']),np.array(traces_summary_sub['v']),np.mean(traces['t']))


# Store R and P
traces_summary_sub['R'] = R
traces_summary_sub['P'] = P

df_traces_summary_sub = pd.DataFrame(traces_summary_sub)
df_traces_summary_group = pd.DataFrame(traces_summary_group)
df_traces_summary_group.to_csv('group_trace_summary.csv',index=False)

df_long_sub = pd.melt(df_traces_summary_sub,id_vars=['subj','Cond'],value_vars=['R','P'])

Stake_primary = []
Stake_secondary = []

for idx,row in df_long.iterrows():
    cond = row['Cond']
    if row['variable'] == 'R':
        Stake_primary.append(cond[1])
        Stake_secondary.append(cond[3])
    else:
        Stake_primary.append(cond[3])
        Stake_secondary.append(cond[1])

df_RP = pd.DataFrame({'subj':df_long['subj'],
                           'Valence':df_long['variable'],
                           'Weight':df_long['value'],
                           'Stake_primary':Stake_primary,
                           'Stake_secondary':Stake_secondary})

df_RP.to_csv('RP.csv',index=False)
