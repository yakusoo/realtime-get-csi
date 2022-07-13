# arg1: input_filename .npy
# arg2: model_filename .sav
import sys
import numpy as np
from sklearn import neighbors
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os
#input_filename1 = '20181026_test_model1.npy'
input_filename1 = sys.argv[1]

def svm_model(input1):
    filename1 = input1
    if os.path.exists(filename1):
        train1 = np.load(filename1)
        train1 = train1.tolist()
    model1 = LinearSVC(C=1.0)

    model1.fit(train1[0], train1[1])

    pickle.dump(model1, open(sys.argv[2], 'wb'))
# pickle.dump(model1, open('SVM_demo_model1.sav', 'wb'))

svm_model(input_filename1)

