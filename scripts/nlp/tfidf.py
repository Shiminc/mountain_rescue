# If smooth_idf=True (the default), the constant “1” is added to the numerator and denominator of the idf as if an extra document was seen containing every term in the collection exactly once, which prevents zero divisions: 
# idf(t) = log [ (1 + n) / (1 + df(t)) ] + 1.

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data
import pandas as pd
import altair as alt
import json

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def fit_vectorizer(docs):
    vectorizer = TfidfVectorizer(min_df=1).fit(docs)
    return vectorizer

def construct_corpus():
    data = preprocess_data()
    sample = data.iloc[1:1000]
    docs = sample.main_text
    new_doc = data.iloc[0].main_text
    return new_doc, docs


def find_matched_vector(new_doc, docs, vectorizer):
    new_doc_vector = vectorizer.transform([new_doc])
    docs_vector = vectorizer.transform(docs)
    relevance_array = cosine_similarity(docs_vector, new_doc_vector)
    max_cos_similarity = max(relevance_array)
    max_doc_index = np.argmax(relevance_array)
    min_cos_similarity = min(relevance_array)
    min_doc_index = np.argmin(relevance_array)
    top_3 = np.argsort(relevance_array.squeeze())[-3:0]
    return max_cos_similarity, docs[max_doc_index], min_cos_similarity,docs[min_doc_index], top_3
def main():
    set_up_altair()
    new_doc, docs = construct_corpus()
    print(new_doc)
    vectorizer = fit_vectorizer(docs)
    print(find_matched_vector(new_doc, docs, vectorizer))
    print('finish')

main()