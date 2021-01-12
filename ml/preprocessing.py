import re
import unicodedata

import pymorphy2 as pymorphy2
import nltk
# sample_sentences = "Привет Миру! Как твои дела? Сегодня неплохая погода."
# if __name__ == '__main__':
#     nlp = ru2.load_ru2('ru2')
#     nlp.add_pipe(nlp.create_pipe('sentencizer'), first=True)
#     doc = nlp(sample_sentences)
#     for s in doc.sents:
#     	print(list(['lemma "{}" from text "{}"'.format(t.lemma_, t.text) for t in s]))
from nltk import text

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from sklearn.pipeline import Pipeline, FeatureUnion

from nltk.corpus import stopwords
from numpy import unicode
from senticnet.babelsenticnet import BabelSenticNet
from sklearn.feature_extraction import text as t

class clean:
    def __init__(self):
        self.regex_dict = {
            'URL': r"""(?xi)\b(?:(?:https?|ftp|file):\/\/|www\.|ftp\.|pic\.|twitter\.|facebook\.)(?:\([-A-Z0-9+&@#\/%=~_|$?!:;,.]*\)|[-A-Z0-9+&@#\/%=~_|$?!:;,.])*(?:\([-A-Z0-9+&@#\/%=~_|$?!:,.]*\)|[A-Z0-9+&@#\/%=~_|$])""",
            'EMOJI': u'([\U0001F1E0-\U0001F1FF])|([\U0001F300-\U0001F5FF])|([\U0001F600-\U0001F64F])|([\U0001F680-\U0001F6FF])|([\U0001F700-\U0001F77F])|([\U0001F800-\U0001F8FF])|([\U0001F900-\U0001F9FF])|([\U0001FA00-\U0001FA6F])|([\U0001FA70-\U0001FAFF])|([\U00002702-\U000027B0])|([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])',
            #'HASHTAG': r"\#\b[\w\-\_]+\b",
            'EMAIL': r"(?:^|(?<=[^\w@.)]))(?:[\w+-](?:\.(?!\.))?)*?[\w+-]@(?:\w-?)*?\w+(?:\.(?:[a-z]{2,})){1,3}(?:$|(?=\b))",
            #'MENTION': r"@[A-Za-z0-9]+",
            'CASHTAG': r"(?:[$\u20ac\u00a3\u00a2]\d+(?:[\\.,']\d+)?(?:[MmKkBb](?:n|(?:il(?:lion)?))?)?)|(?:\d+(?:[\\.,']\\d+)?[$\u20ac\u00a3\u00a2])",
            'DATE': r"(?:(?:(?:(?:(?<!:)\b\'?\d{1,4},? ?)?\b(?:[Jj]an(?:uary)?|[Ff]eb(?:ruary)?|[Mm]ar(?:ch)?|[Aa]pr(?:il)?|May|[Jj]un(?:e)?|[Jj]ul(?:y)?|[Aa]ug(?:ust)?|[Ss]ept?(?:ember)?|[Oo]ct(?:ober)?|[Nn]ov(?:ember)?|[Dd]ec(?:ember)?)\b(?:(?:,? ?\'?)?\d{1,4}(?:st|nd|rd|n?th)?\b(?:[,\\/]? ?\'?\d{2,4}[a-zA-Z]*)?(?: ?- ?\d{2,4}[a-zA-Z]*)?(?!:\d{1,4})\b))|(?:(?:(?<!:)\b\\'?\d{1,4},? ?)\b(?:[Jj]an(?:uary)?|[Ff]eb(?:ruary)?|[Mm]ar(?:ch)?|[Aa]pr(?:il)?|May|[Jj]un(?:e)?|[Jj]ul(?:y)?|[Aa]ug(?:ust)?|[Ss]ept?(?:ember)?|[Oo]ct(?:ober)?|[Nn]ov(?:ember)?|[Dd]ec(?:ember)?)\b(?:(?:,? ?\'?)?\d{1,4}(?:st|nd|rd|n?th)?\b(?:[,\\/]? ?\'?\d{2,4}[a-zA-Z]*)?(?: ?- ?\d{2,4}[a-zA-Z]*)?(?!:\d{1,4})\b)?))|(?:\b(?<!\d\\.)(?:(?:(?:[0123]?[0-9][\\.\\-\\/])?[0123]?[0-9][\\.\\-\\/][12][0-9]{3})|(?:[0123]?[0-9][\\.\\-\\/][0123]?[0-9][\\.\\-\\/][12]?[0-9]{2,3}))(?!\.\d)\b))",
            'TIME': r'(?:(?:\d+)?\\.?\d+(?:AM|PM|am|pm|a\\.m\\.|p\\.m\\.))|(?:(?:[0-2]?[0-9]|[2][0-3]):(?:[0-5][0-9])(?::(?:[0-5][0-9]))?(?: ?(?:AM|PM|am|pm|a\\.m\\.|p\\.m\\.))?)',
            'EMPHASIS': r"(?:\*\b\w+\b\*)",
            'ELONG': r"\b[A-Za-z]*([a-zA-Z])\1\1[A-Za-z]*\b"}
        
        self.emoticons = {
            ':*': 'поцелуй',
            ':-*': 'поцелуй',
            ':x': 'поцелуй',
            ':-)': 'счастье',
            ':-))': 'счастье',
            ':-)))': 'счастье',
            ':-))))': 'счастье',
            ':-)))))': 'счастье',
            ':-))))))': 'счастье',
            ':)': 'счастье',
            ':))': 'счастье',
            ':)))': 'счастье',
            ':))))': 'счастье',
            ':)))))': 'счастье',
            ':))))))': 'счастье',
            ':)))))))': 'счастье',
            ':o)': 'счастье',
            ':]': 'счастье',
            ':3': 'счастье',
            ':c)': 'счастье',
            ':>': 'счастье',
            '=]': 'счастье',
            '8)': 'счастье',
            '=)': 'счастье',
            ':}': 'счастье',
            ':^)': 'счастье',
            '|;-)': 'счастье',
            ":'-)": 'счастье',
            ":')": 'счастье',
            '\o/': 'счастье',
            '*\\0/*': 'счастье',
            ':-D': 'смех',
            ':D': 'смех',
            '8-D': 'смех',
            '8D': 'смех',
            'x-D': 'смех',
            'xD': 'смех',
            'X-D': 'смех',
            'XD': 'смех',
            '=-D': 'смех',
            '=D': 'смех',
            '=-3': 'смех',
            '=3': 'смех',
            'B^D': 'смех',
            '>:[': 'грусть',
            ':-(': 'грусть',
            ':-((': 'грусть',
            ':-(((': 'грусть',
            ':-((((': 'грусть',
            ':-(((((': 'грусть',
            ':-((((((': 'грусть',
            ':-(((((((': 'грусть',
            ':(': 'грусть',
            ':((': 'грусть',
            ':(((': 'грусть',
            ':((((': 'грусть',
            ':(((((': 'грусть',
            ':((((((': 'грусть',
            ':(((((((': 'грусть',
            ':((((((((': 'грусть',
            ':-c': 'грусть',
            ':c': 'грусть',
            ':-<': 'грусть',
            ':<': 'грусть',
            ':-[': 'грусть',
            ':[': 'грусть',
            ':{': 'грусть',
            ':-||': 'грусть',
            ':@': 'грусть',
            ":'-(": 'грусть',
            ":'(": 'грусть',
            'D:<': 'грусть',
            'D:': 'грусть',
            'D8': 'грусть',
            'D;': 'грусть',
            'D=': 'грусть',
            'DX': 'грусть',
            'v.v': 'грусть',
            "D-':": 'грусть',
            '(>_<)': 'грусть',
            ':|': 'грусть',
            '>:O': 'сюрприз',
            ':-O': 'сюрприз',
            ':-o': 'сюрприз',
            ':O': 'сюрприз',
            '°o°': 'сюрприз',
            'o_O': 'сюрприз',
            'o_0': 'сюрприз',
            'o.O': 'сюрприз',
            'o-o': 'сюрприз',
            '8-0': 'сюрприз',
            '|-O': 'сюрприз',
            ';-)': 'подмигивание',
            ';)': 'подмигивание',
            '*-)': 'подмигивание',
            '*)': 'подмигивание',
            ';-]': 'подмигивание',
            ';]': 'подмигивание',
            ';D': 'подмигивание',
            ';^)': 'подмигивание',
            ':-,': 'подмигивание',
            '>:P': 'дразниться',
            ':-P': 'дразниться',
            ':P': 'дразниться',
            'X-P': 'дразниться',
            'x-p': 'дразниться',
            ':-p': 'дразниться',
            ':p': 'дразниться',
            '=p': 'дразниться',
            ':-Þ': 'дразниться',
            ':Þ': 'дразниться',
            ':-b': 'дразниться',
            ':b': 'дразниться',
            ':-&': 'дразниться',
            '>:\\': 'раздраженный',
            '>:/': 'раздраженный',
            ':-/': 'раздраженный',
            ':-.': 'раздраженный',
            ':/': 'раздраженный',
            ':\\': 'раздраженный',
            '=/': 'раздраженный',
            '=\\': 'раздраженный',
            ':L': 'раздраженный',
            '=L': 'раздраженный',
            ':S': 'раздраженный',
            '>.<': 'раздраженный',
            ':-|': 'раздраженный',
            '<:-|': 'раздраженный',
            'O:-)': 'ангел',
            '0:-3': 'ангел',
            '0:3': 'ангел',
            '0:-)': 'ангел',
            '0:)': 'ангел',
            '0;^)': 'ангел',
            '>:)': 'демон',
            '>:D': 'демон',
            '>:-D': 'демон',
            '>;)': 'демон',
            '>:-)': 'демон',
            '}:-)': 'демон',
            '}:)': 'демон',
            '3:-)': 'демон',
            '3:)': 'демон',
            'o/\o': 'дай пять',
            '^5': 'дай пять',
            '>_>^': 'дай пять',
            '^<_<': 'дай пять',
            '<3': 'сердце',
            '^3^': 'улыбка',
            "(':": 'улыбка',
            " > < ": 'улыбка',
            "UvU": 'улыбка',
            "uwu": 'улыбка',
            'UwU': 'улыбка'
        }

    def get_compiled(self):
        regexes = {k: re.compile(self.regex_dict[k]) for k, v in
                   self.regex_dict.items()}
        return regexes

    def fit(self, Example):
        regex = self.get_compiled()
        for key, reg in regex.items():
            Example = regex[key].sub(lambda m: " <" + key + "> ",
                                               Example)
        for word in self.emoticons.keys():
            Example = Example.replace(word, self.emoticons[word])
        Example = Example.lower()
        Example = re.sub(r"[\-\"`@#$%^&*(|)/~\[\]{\}:;+,._='!?]+", " ", Example)
        Example = unicodedata.normalize('NFKD', Example).encode('ascii', errors='ignore').decode('utf8',
                                                                                                 errors='ignore')
        Example = re.sub(r'\b([b-hB-Hj-zJ-Z] )', ' ', Example)
        Example = re.sub(r'( [b-hB-Hj-zJ-Z])\b', ' ', Example)
        Example = ' '.join(Example.split())
        return Example

stop = stopwords.words('russian')
def russian_emotion(text_ru):
    #normalization

    # stemmatization doesn't work
    # from nltk.stem.snowball import SnowballStemmer
    # stemmer = SnowballStemmer("russian")
    # words = [stemmer.stem(word) for (word, pos) in pos_tag(word_tokenize(text_ru)) if word == "не" or word not in stop]
    # print(words)

    #lemmatization. Not remove word "не" for using in syntactic feature
    text_ru = " ".join(word.lower() for word in text_ru.split()) #lowercasing
    text_ru = re.sub('\-\s\r\n\s{1,}|\-\s\r\n|\r\n', '', text_ru) #deleting newlines and line-breaks
    cleaner = clean()
    text_ru = cleaner.fit(text_ru)
    words = [pymorphy2.MorphAnalyzer().parse(unicode(word))[0].normal_form for word in text_ru.split() if word == "не" or word not in stop]
    emotions = {'интерес' : 0, 'радость' : 0, 'восхищение' : 0, 'гнев' : 0, 'отвращение' : 0, 'попугать' : 0,
                'сюрприз' : 0, 'печаль' : 0}
    countNo = 0
    sign = 1
    sn = BabelSenticNet('ru')
    for word in words:
        if word == 'не':
            sign = -1
            countNo += 1
        else:
            if (word in sn.data):
                ems = sn.moodtags(word)
                emotions[ems[0][1:]] += sign
                emotions[ems[1][1:]] += sign
            if sign == -1:
                sign = 1
    for e in emotions.keys():
        emotions[e] /= (len(words) - countNo)

    print(words)
    return (words, emotions.values())


def textsPrepocessing(texts):
    return [russian_emotion(text) for text in texts]