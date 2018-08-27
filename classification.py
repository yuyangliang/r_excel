# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 11:20:57 2018

@author: Yuyang
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn import preprocessing
from sklearn.model_selection import cross_validate
from sklearn.tree import export_graphviz
from sklearn import metrics

alldat = pd.read_csv('data/prediction_data_7.csv')
labels = np.array(alldat.unsolved)
alldat = alldat.drop(['unsolved'], axis = 1)
feature_names = list(alldat.columns)
features = np.array(alldat)

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.2, random_state = 4040)

rf = RandomForestClassifier(n_estimators = 1000, random_state = 4040)
rf = RandomForestClassifier(n_estimators = 1000, random_state = 4040, max_depth = 5)
rf.fit(train_features, train_labels)
predictions = rf.predict(test_features)
rf.fit(scaled_train_features, train_labels)
predictions = rf.predict(scaled_test_features)

cv_results = cross_validate(rf, features, labels, scoring = ['accuracy', 'f1_weighted', 'roc_auc'], cv = 5)
cv_results['test_accuracy'].mean()
cv_results['test_roc_auc'].mean()
cv_results['test_f1_weighted'].mean() 


tree = rf.estimators_[89]
export_graphviz(tree, out_file = 'tree.dot', feature_names = feature_names, class_names = ['0', '1'], rounded = True, precision = 1)
(graph, ) = pydot.graph_from_dot_file('tree.dot')
graph.write_png('tree.png');

print(classification_report(test_labels, predictions))
importances = list(rf.feature_importances_)
feature_importance = pd.DataFrame(list(zip(feature_names, importances)), columns = ['names', 'importance'])
feature_importance.to_csv('feature_importance3.csv', index = False)