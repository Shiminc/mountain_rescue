import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.plot import set_up_altair
from utils.utils import preprocess_data
import pandas as pd
import altair as alt
import json

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

def createWordVector(tokenized_docs,lemmatized=False):

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
    df = df.fillna(0).astype(int)

    return df

def main():
    set_up_altair()
    data = preprocess_data()
    docs = data.main_text.iloc[0:5]
    tokenized_docs = [nlp(doc) for doc in docs]

    createWordVector(tokenized_docs,lemmatized=False)
    print('finish')



main()