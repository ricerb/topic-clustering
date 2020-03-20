from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re


stop_words = set(stopwords.words("english"))
ps = PorterStemmer()


def stem_and_tokenize(words):
    tokens = word_tokenize(words)

    stemmed_words = []
    for word in tokens:
        stemmed_words.append(ps.stem(word))

    stopword_filtered = [w for w in stemmed_words if w not in stop_words]

    # remove digits and punctuation
    pattern = re.compile(r"[a-zA-Z]+")
    cleaned = [x for x in stopword_filtered if pattern.search(x)]

    # turn list into string separated by spaces
    export = ' '.join(cleaned)

    return export