from matplotlib import pyplot as plt
from sklearn import datasets
import numpy as np
import csv
import json
from sklearn import cluster
from sklearn import neighbors
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os
import sys
from statistics import mode
import matplotlib.pyplot as plt
import matplotlib
import pandas

def svm_check(input_file1, modelfile):

#    filename1 = 'SVM_demo_model1.sav'
    label1 = []
    if os.path.exists(modelfile):
        model1 = pickle.load(open(modelfile, 'rb'))
    else:
        print("No such a file")
        sys.exit()

    if len(input_file1) != 0:
        #for i in range(len(input_file1[0])):
        #    label1.append(label)
        #for i in range(len(input_file1)):
        pred1 = model1.predict(input_file1[0])
        pred1 = pred1.tolist()
        #print(pred1)
        score_svm = mode(pred1)
        score_per = pred1.count(score_svm) * 100 / len(pred1)
        f = open('./results/result.txt', 'w')
        f.write('%d\n' % (score_svm))
        f.write('%d\n' % (score_per))
        f.write('%d\n' % (len(pred1)))
        f.close()
        for i in range(7):
            print("SVM_%d is %f" % (i, pred1.count(i) * 100 / len(pred1)))
        #print("SVMの正答率: %f"%(accuracy_score(label1, pred1)))
    #return accuracy_score(label1, pred1)

def error():
    f = open('./results/result.txt', 'w')
    score_svm = -100
    f.write('%d\n' % (score_svm))
    f.write('%d\n' % (score_svm))
    f.write('0\n')
    f.close()
