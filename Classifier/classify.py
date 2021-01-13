import pickle

import langid
import numpy
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.feature_extraction import text

from Classifier.preprocessing import textsPrepocessing


def lang(doc):
    l, _ = langid.classify(doc)
    return l


def classify(test_filename):
    test_doc = pd.read_csv(test_filename, header=0)

    test = []
    label_encoder = pickle.load(open('encoder.sav', 'rb'))
    label_all = label_encoder.fit_transform(test_doc['emotion'])
    label = []
    for i, doc in enumerate(test_doc['post']):
        if lang(doc) == 'ru':
            test.append(doc)
            label.append(label_all[i])

    test = textsPrepocessing(test)

    ngrams_vectorizer = pickle.load(open('ngrams.sav', 'rb'))

    test_features = csr_matrix(numpy.hstack(([emo for (emo, w) in test], ngrams_vectorizer.fit_transform([''.join(w) for (emo, w) in test]).toarray())))

    best_model = pickle.load(open('model.sav', 'rb'))
    return (label_encoder.inverse_transform(best_model.predict(test_features)))
