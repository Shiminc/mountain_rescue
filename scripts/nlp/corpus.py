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
from string import punctuation
# Load English tokenizer, tagger, parser and NER
# The “sm” here stands for “small” (17 MB), “md” for “medium” (45 MB), and“lg” for “large” (780 MB).
nlp = spacy.load('en_core_web_sm')

# to know what is involved in the pipelines and rules of spacy
# nlp.pipe_names
# nlp.pipe_labels

# to disable some of the tokeniser
# nlp = spacy.load('en_core_web_sm', disable=nlp.pipe_names)

def createSkVector(docs):
    vectorizer = CountVectorizer(ngram_range=(1, 2)).fit(docs)
    count_vectors = vectorizer.transform(docs)
    vocabulary = vectorizer.get_feature_names_out()
    return vocabulary, vectorizer, count_vectors

def qualitative_comparison(vocabulary,skVector_matrix,doc1,doc2):
    count_array = skVector_matrix[(doc1,doc2),:].toarray()
    count_df = pd.DataFrame(count_array).T
    count_df.set_index(vocabulary,inplace=True)
    # drop 0 for both doc
    count_df = count_df.loc[count_df.sum(axis=1)!=0]
    return count_df

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

def find_doc_close_to_new_doc(vectorizer, new_doc, skVector_matrix):
    new_doc_vector = vectorizer.transform([new_doc])
    max_cos_similarity = max(cosine_similarity(skVector_matrix, new_doc_vector))
    max_doc_index = np.argmax(cosine_similarity(skVector_matrix, new_doc_vector))
    min_cos_similarity = min(cosine_similarity(skVector_matrix, new_doc_vector))
    min_doc_index = np.argmin(cosine_similarity(skVector_matrix, new_doc_vector))
    return max_cos_similarity, max_doc_index, min_cos_similarity, min_doc_index

def main():
    set_up_altair()
    print(punctuation)
    data = preprocess_data()
    sample = data.iloc[0:10]
    docs = sample.main_text
    new_doc = data.iloc[11].main_text


    # sklearn, subjected to default setting/pipelines
    vocabulary, vectorizer, skVector_matrix = createSkVector(docs)
    print(find_doc_close_to_new_doc(vectorizer, new_doc, skVector_matrix))

    # observation = qualitative_comparison(vocabulary,skVector_matrix,8,9)  
    # observation.to_csv('observation_low.csv')
    # cf0n1 = cosine_similarity(skVector_matrix[9,:],skVector_matrix[8,:])
    # print(cf0n1)
    # # spacy and manual vectorizing 
    # tokenized_docs = [nlp(doc) for doc in docs]
    # wordVector_df = createWordVector(tokenized_docs,lemmatized=False)
    
    print('finish')



main()