#!/usr/bin/env python
import csv
from sklearn import svm
import numpy as np
import scipy.sparse as sp
import sys
from sklearn.externals import joblib
from mlloutils import expand_to_vectors

if len(sys.argv) < 3:
  print >> sys.stderr, 'Usage: python '+sys.argv[0]+' <training csv input> <persistent model output>'
  exit(0)

# Grab the training data
training_name = sys.argv[1]
print >> sys.stderr, 'Loading training set from '+training_name
training_vectors, training_target = expand_to_vectors(training_name, [6, 7, 8], 9)

# Create a naive classifier
clf = svm.sparse.SVC()
print >> sys.stderr, 'Training classifier...'
clf.fit(training_vectors, training_target)

model_name = sys.argv[2]
print >> sys.stderr, 'Saving classifier to '+model_name
joblib.dump(clf, model_name) 
