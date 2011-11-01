#!/usr/bin/env python
import csv
from sklearn import svm
import numpy as np
import scipy.sparse as sp
import sys
from sklearn.externals import joblib
from mlloutils import expand_to_vectors

if len(sys.argv) < 2:
  print >> sys.stderr, 'Usage: python '+sys.argv[0]+' <test csv input> <persistent model input>'
  exit(0)

model_name = sys.argv[2]
print >> sys.stderr, 'Loading classifier from '+model_name
clf = joblib.load(model_name) or die('Couldn\'t load model from '+model_name)

test_name = sys.argv[1]
print >> sys.stderr, 'Loading test set from '+test_name
test_vectors, ids = expand_to_vectors(test_name, [6, 7, 8], 0)

print >> sys.stderr, 'Predicting...'
prediction_matrix = clf.predict(test_vectors)
prediction = prediction_matrix.tolist()

print 'id,good'
for index, value in enumerate(ids):
  print str(value)+','+str(prediction[index])