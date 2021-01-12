import pickle

import langid
import pandas as pd
from sklearn.feature_extraction import text


def classify(test_filename):
    test_doc = pd.read_csv(test_filename, header=0)

    test = textPreprocessing([doc for doc in test_doc[0] if langid.classify(doc)[0] == 'ru'])

    ngrams_vectorizer = pickle.load(open('ngrams.sav', 'rb'))

    test_features = [e + wn for (e, wn) in zip([emo for (emo, w) in test],
                                                ngrams_vectorizer.transform([''.join(w) for (emo, w) in test]))]

    label_encoder = pickle.load(open('encoder.sav', 'rb'))

    filename = 'encoder.sav'
    pickle.dump(label_encoder, open(filename, 'wb'))

    best_model = pickle.load(open('model.sav', 'rb'))
    return (label_encoder.inverse_transform(best_model.predict(test_features)))