#!/usr/bin/env python
from sklearn import utils
from sklearn import metrics
from sklearn import linear_model
from sklearn import svm
from sklearn import grid_search
from sklearn import pipeline
import numpy as np
import sys
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.externals import joblib
from mlloutils import expand_to_vectors

if len(sys.argv) < 3:
  print >> sys.stderr, ('Usage: python ' + sys.argv[0]
                        + ' <training csv input> <persistent model output>')
  exit(0)

# Grab the training data
training_name = sys.argv[1]
print >> sys.stderr, 'Loading training set from '+training_name
training_vectors, training_target = expand_to_vectors(
    training_name, [6, 7, 8], 9)
print "%d vectors with dimension %d" % training_vectors.shape

# Normalize the sparse positive features using the TF-IDF normalizer as field
# 6, 7 and 8 are word occurrences in text fields
tfidf = TfidfTransformer()
training_vectors = tfidf.fit_transform(training_vectors)

# Shuffle the samples as SGD models assume i.i.d.
training_vectors, training_target = utils.shuffle(
    training_vectors, training_target, random_state=0)

# Create a naive classifier
models = [
    (linear_model.sparse.SGDClassifier(n_iter=5),
     {'alpha': np.logspace(-7, -4, 5)}),
#    (svm.sparse.LinearSVC(),
#     {'C': np.logspace(4, 7, 5)}),
]

# Uncomment the previous lines if you want to use liblinear to fit a LinearSVC model
# (much slower than SGD without improvement)

best_score = None
best_clf = None

for clf, grid in models:
    msg = 'Training model %r using grid search for best hyper-param: %r' % (
        clf, grid)
    print >> sys.stderr, msg
    gs = grid_search.GridSearchCV(
        clf, grid, score_func=metrics.f1_score, verbose=1,
        fit_params={'class_weight': 'auto'})
    gs.fit(training_vectors, training_target)
    print "Best model: %r" % gs.best_estimator
    print "Best score: %0.3f" %  gs.best_score
    if best_clf is None or best_score < gs.best_score:
        best_clf = gs.best_estimator
        best_score = gs.best_score

model_name = sys.argv[2]
print >> sys.stderr, 'Saving classifier to ' + model_name

# combine the normalizer and the classifier in a compound model so that the
# same normalization will be applied as a preprocessing on the test set
p = pipeline.Pipeline([('tfidf', tfidf), ('clf', best_clf)])
joblib.dump(p, model_name)
