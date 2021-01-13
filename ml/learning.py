import pickle

import langid as langid
import numpy
import pandas as pd

from ml.preprocessing import textsPrepocessing
from scipy.sparse import csr_matrix
from sklearn.feature_extraction import text
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import FeatureUnion,Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC


def lang(doc):
    l, _ = langid.classify(doc)
    return l


def learn(train_file):
    train_doc = pd.read_csv('Train.csv',header=0)

    train = []
    label_encoder = LabelEncoder()
    label_all = label_encoder.fit_transform(train_doc['emotion'])
    label = []
    for i, doc in enumerate(train_doc['post']):
        if lang(doc) == 'ru':
            train.append(doc)
            label.append(label_all[i])

    train = textsPrepocessing(train)

    word_vectorizer = text.TfidfVectorizer(
        analyzer='word', ngram_range=(1, 3),
        min_df=2, use_idf=True, sublinear_tf=True)
    char_vectorizer = text.TfidfVectorizer(
        analyzer='char', ngram_range=(3, 5),
        min_df=2, use_idf=True, sublinear_tf=True)
    ngrams_vectorizer = Pipeline(
        [('feats', FeatureUnion([('word_ngram', word_vectorizer), ('char_ngram', char_vectorizer),
                                 ])), ])

    train_features = csr_matrix(numpy.hstack(([emo for (emo, w) in train], ngrams_vectorizer.fit_transform([''.join(w) for (emo, w) in train]).toarray())))
    #train_features = [e + wn for (e, wn) in zip([emo for (emo, w) in train], ngrams_vectorizer.fit_transform([''.join(w) for (emo, w) in train]))]
    filename = 'ngrams.sav'
    pickle.dump(ngrams_vectorizer, open(filename, 'wb'))



    filename = 'encoder.sav'
    pickle.dump(label_encoder, open(filename, 'wb'))

    best_model = LinearSVC(class_weight='balanced')
    f1_best = cross_val_score(best_model, train_features, label, cv=10, scoring='f1_macro').mean()
    print(f1_best)

    for i in range(10, 100, 5):
        model = KNeighborsClassifier(n_neighbors=10, weights='distance')
        f1 = cross_val_score(model, train_features, label, cv=10, scoring='f1_macro').mean()
        print(f1)
        if (f1 > f1_best):
            best_model = model
            f1_best = f1

    filename = 'model.sav'
    pickle.dump(best_model, open(filename, 'wb'))


learn('Train.csv')