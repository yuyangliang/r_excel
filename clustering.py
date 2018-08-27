# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 15:34:26 2016

@author: Yuyang
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
%matplotlib qt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from scipy.stats import itemfreq
import matplotlib 
from sklearn.mixture import GaussianMixture 
    
uprof_df_all = pd.read_csv('data/kmdata_discretized.csv')
uprof_df = uprof_df_all.drop('time_window', axis = 1)

Ks = range(2, 11)
gmm = [GaussianMixture(n_components = k, covariance_type = 'full', n_init = 5, random_state = 4040) for k in Ks]
BIC = [i.fit(uprof_df).bic(uprof_df) for i in gmm]
matplotlib.rcParams.update({'font.size': 25})
plt.plot(Ks, BIC, color = '#6666ff', marker = 'o', markersize = 10, linewidth = 3) 
plt.xlabel('Number of Clusters')
plt.ylabel('BIC score')
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText = True, useOffset = True)

BICs = []
for j in range(1, 15):    
    uprof_df = uprof_df_all[uprof_df_all['time_window'] == j].drop('time_window', axis = 1)
    BICs.append([-i.fit(uprof_df).score(uprof_df) for i in km])
    plt.subplot(5, 3, j)
    plt.plot(Ks, BICs[-1], 'bo', Ks, BICs[-1], 'b')

Ks = range(2, 11)
gmm = [GaussianMixture(n_components = k, covariance_type = 'full', n_init = 5, random_state = 4040) for k in Ks]
BIC = [i.fit(uprof_df.iloc[:, 0:8]).bic(uprof_df.iloc[:, 0:8]) for i in gmm]
plt.plot(Ks, BIC, 'bo', Ks, BIC, 'b')

def get_center(nc):
    cp_center = pd.DataFrame(gmm[nc].means_)
    cp_center.columns = list(uprof_df)
    labels = pd.DataFrame(gmm[nc].predict(uprof_df), columns = ['labels'])
    cp_center['percent'] = [i[1]*100/float(uprof_df.shape[0]) for i in itemfreq(labels)]
    return (cp_center, labels)

(cp_center, labels) = get_center(4)

#Produce the plot
cp_center = cp_center.rename(columns = {'cscorem': 'Avg_R_Score', 'clenm': 'Avg_R_Length', 'cspep': 'Pct_R_Special', 
                            'sscorem': 'Avg_Q_Score', 'slenm': 'Avg_Q_Length', 'sspep': 'Pct_Q_Special', 
                            'qtimes': 'Num_Q', 'timem': 'Avg_R_Timerank', 'depthm': 'Avg_R_Depth', 
                            'flv': 'Num_R_Direct', 'iodiff': 'Diff_In_Out', 'out_num': 'Out'})
label_order = ['Avg_R_Score', 'Avg_R_Length', 'Pct_R_Special', 'Avg_R_Timerank', 'Avg_R_Depth', 'Num_R_Direct',
               'Avg_Q_Score', 'Avg_Q_Length', 'Pct_Q_Special', 'Num_Q', 'Diff_In_Out', 'Out']

fig, axes = plt.subplots(nrows = 2, ncols = 3, sharey = True)
plt.subplots_adjust(hspace = 0.3)
ax1 = cp_center.iloc[0, :-1].loc[label_order].plot(kind = 'barh', color = '#6666ff', ax = axes[0,0], xlim = (-1, 1.5), title = 'Frequent Questioner ')
ax2 = cp_center.iloc[2, :-1].loc[label_order].plot(kind = 'barh', color = '#6666ff', ax = axes[0,1], xlim = (-1, 1.5), title = 'Occasional Questioner')
ax3 = cp_center.iloc[1, :-1].loc[label_order].plot(kind = 'barh', color = '#6666ff', ax = axes[0,2], xlim = (-1, 1.5), title = 'Occasional Answerer')
ax4 = cp_center.iloc[3, :-1].loc[label_order].plot(kind = 'barh', color = '#6666ff', ax = axes[1,0], xlim = (-2, 3), title = 'Community Activist')
ax5 = cp_center.iloc[4, :-1].loc[label_order].plot(kind = 'barh', color = '#6666ff', ax = axes[1,1], xlim = (-1, 2), title = 'Elaborative Questioner ')
ax6 = cp_center.iloc[5, :-1].loc[label_order].plot(kind = 'barh', color = '#6666ff', ax = axes[1,2], xlim = (-1, 2), title = 'Experienced Answerer')