import pickle

import langid as langid
import pandas as pd

from preprocessing import textPreprocessing
from sklearn.feature_extraction import text
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import FeatureUnion,Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC


def learn(train_file):
    train_doc = pd.read_csv('Train.csv',header=0)

    train = textPreprocessing([doc for doc in train_doc[0] if langid.classify(doc)[0] == 'ru'])

    word_vectorizer = text.TfidfVectorizer(
        analyzer='word', ngram_range=(1, 3),
        min_df=2, use_idf=True, sublinear_tf=True)
    char_vectorizer = text.TfidfVectorizer(
        analyzer='char', ngram_range=(3, 5),
        min_df=2, use_idf=True, sublinear_tf=True)
    ngrams_vectorizer = Pipeline(
        [('feats', FeatureUnion([('word_ngram', word_vectorizer), ('char_ngram', char_vectorizer),
                                 ])), ])

    train_features = [e + wn for (e, wn) in zip([emo for (emo, w) in train], ngrams_vectorizer.fit_transform([''.join(w) for (emo, w) in train]))]
    filename = 'ngrams.sav'
    pickle.dump(ngrams_vectorizer, open(filename, 'wb'))

    label_encoder = LabelEncoder()
    label = label_encoder.fit_transform(train_doc[1])

    filename = 'encoder.sav'
    pickle.dump(label_encoder, open(filename, 'wb'))

    best_model = LinearSVC(class_weight='balanced')
    f1_best = cross_val_score(best_model, train_features, label, cv=10, scoring='f1_macro').mean()

    for i in range(10, 100, 5):
        model = KNeighborsClassifier(n_neighbors=10, weights='distance')
        f1 = cross_val_score(best_model, train_features, label, cv=10, scoring='f1_macro').mean()
        if (f1 > f1_best):
            best_model = model
            f1_best = f1

    filename = 'model.sav'
    pickle.dump(best_model, open(filename, 'wb'))