import pickle

import langid
import numpy
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.feature_extraction import text

from ml.preprocessing import textsPrepocessing


def classify(test_filename):
    test_doc = pd.read_csv(test_filename, header=0)

    test = textsPrepocessing([doc for doc in test_doc[0] if langid.classify(doc)[0] == 'ru'])

    ngrams_vectorizer = pickle.load(open('ngrams.sav', 'rb'))

    test_features = csr_matrix(numpy.hstack(([emo for (emo, w) in test], ngrams_vectorizer.fit_transform([''.join(w) for (emo, w) in test]).toarray())))

    label_encoder = pickle.load(open('encoder.sav', 'rb'))

    filename = 'encoder.sav'
    pickle.dump(label_encoder, open(filename, 'wb'))

    best_model = pickle.load(open('model.sav', 'rb'))
    return (label_encoder.inverse_transform(best_model.predict(test_features)))