import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data
import pandas as pd
import altair as alt
import json

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import spacy

# Load English tokenizer, tagger, parser and NER
# The “sm” here stands for “small” (17 MB), “md” for “medium” (45 MB), and“lg” for “large” (780 MB).
nlp = spacy.load('en_core_web_sm')

# to know what is involved in the pipelines and rules of spacy
# nlp.pipe_names
# nlp.pipe_labels

# to disable some of the tokeniser
# nlp = spacy.load('en_core_web_sm', disable=nlp.pipe_names)

def createSkVector(docs):
    vectorizer = CountVectorizer().fit(docs)
    count_vectors = vectorizer.transform(docs)
    return count_vectors


def createWordVector(tokenized_docs,lemmatized=False):
# manually create vector
    # to collect word_counts of every doc
    word_counts = []
    # go through each doc
    for doc in tokenized_docs:
        # to collect all token texts in the doc
        tokens = [] 
        # only lower-case non proper-noun
        for token in doc:
            if token.pos_=='PROPN':
                # Whether to use lemma or text
                if lemmatized:
                    tokens.append(token.lemma_)
                else:
                    tokens.append(token.text)
            else:
                if lemmatized:
                    tokens.append(token.lemma_)
                else:
                    tokens.append(token.text.lower())
        # Counter(tokens) is a dict
        word_counts.append(Counter(tokens))

    df = pd.DataFrame(word_counts)
    # transpose so word is the index then sort it then transpose back
    df = df.T.sort_index().T
    df = df.fillna(0).astype(int)

    return df

def main():
    set_up_altair()
    data = preprocess_data()
    docs = data.main_text.iloc[0:5]

    # sklearn, subjected to default setting/pipelines
    skVector_matrix = createSkVector(docs)
    cf0n1 = cosine_similarity(skVector_matrix[0,:],skVector_matrix[1,:])
    print(cf0n1)
    # spacy and manual vectorizing 
    tokenized_docs = [nlp(doc) for doc in docs]
    wordVector_df = createWordVector(tokenized_docs,lemmatized=False)
    
    print('finish')



main()