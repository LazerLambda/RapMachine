#!/usr/bin/python3



"""Script for keyword extraction with the TF-IDF algorithm."""


import json
import re
import spacy

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class KeywordExtractor(object):

  # download spacy package in terminal with 'python -m spacy download en_core_web_md' command
  spacy_nlp = spacy.load('en_core_web_md')

  def __init__(self, path):
    self.path = path

  def load_data(self):
  
    with open(self.path, 'r', encoding='utf-8') as json_file:
      data = json.load(json_file)
  
    return data


  def prepare_corpus(self):
  
    data = self.load_data()
    lemmatized_corpus = []
    corpus = list(data.values())
    for song in corpus:
      doc = self.lemmatize_document(song)
      lemmatized_corpus.append(doc)

    return lemmatized_corpus


  def lemmatize_document(self, document):
    doc = self.spacy_nlp(document.lower())
    lemmas = [
                token.lemma_ 
                for token in doc
                if (not token.is_stop)
                and (not token.is_punct)
                and (not token.like_num)
                if len(token) > 3
              ]

    return " ".join(lemmas)


  def replace_non_alnum(self, corpus):
    clean_corpus = []
    for word in corpus:
      w = re.sub(r'\d+|[^\w\s]', '', word)
      clean_corpus.append(w)

    return clean_corpus


  def extract_keywords(self, corpus, document, top_n):

    tfidf_vectorizer = TfidfVectorizer()
    word_count_matrix = tfidf_vectorizer.fit_transform(corpus)
    feature_array = np.array(tfidf_vectorizer.get_feature_names_out())
    doc = tfidf_vectorizer.transform([document])
    tfidf_sorting = np.argsort(doc.toarray()).flatten()[::-1]
    keywords = feature_array[tfidf_sorting][:top_n]
  
    return keywords


if __name__ == "__main__":
  keyword_extractor = KeywordExtractor("path_to_json_file")
  data = keyword_extractor.prepare_corpus()
  clean_data = keyword_extractor.replace_non_alnum(data)
  test_doc = keyword_extractor.lemmatize_document("document_string")
  keywords = keyword_extractor.extract_keywords(clean_data, test_doc, 5)
  print(keywords)