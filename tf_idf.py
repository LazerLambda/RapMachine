#!/usr/bin/python3



"""Script for keyword extraction with the TF-IDF algorithm."""


import json
import os
import pickle
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
    """Load rap data from JSON.

    Returns:
        JSON file
    """
    with open(self.path, 'r', encoding='utf-8') as json_file:
      data = json.load(json_file)
  
    return data


  def prepare_corpus(self, data):
    """Preprocess loaded data.

    Args:
        data (dict): dictionary of songs and their verses

    Returns:
        list: list of lemmatized verses without
        stopwords, punctuation and numbers
    """
    lemmatized_corpus = []
    corpus = list(data.values())
    for song in corpus:
      doc = self.lemmatize_document(song)
      lemmatized_corpus.append(doc)

    return lemmatized_corpus


  def lemmatize_document(self, document):
    """Lemmatize single document for preprocessing.

    Args:
        document (str): document for lemmatizing

    Returns:
        str: lemmatized document
    """
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
    """Remove non alphanumeric values from strings.

    Args:
        corpus (list): list of documents

    Returns:
        list: same list of documents without noisy words
    """
    clean_corpus = []
    for word in corpus:
      w = re.sub(r'\d+|[^\w\s]', '', word)
      clean_corpus.append(w)

    return clean_corpus


  def convert_to_nouns(self, corpus):
    """Filter nouns from corpus for better keyword extraction.

    Args:
        corpus (list): list of documents

    Returns:
        list: list of documents with only nouns remaining
    """
    filtered_by_nouns = []
    for text in corpus:
      doc = self.spacy_nlp(text)
      nouns_list = [
                    token.text
                    for token in doc
                    if token.pos_ == "NOUN"
      ]
      if len(nouns_list) > 0:
        filtered_by_nouns.append(" ".join(nouns_list))
      
    return filtered_by_nouns
  

  def save_tfidf_model(self, filename, model):
    """Save generated TFIDF model.

    Args:
        filename (str): name of file to save model
        model (sklearn.feature_extraction.text.TfidfVectorizer): TFIDF model
    """
    with open(filename, 'wb') as tfidf_model:
      pickle.dump(model, tfidf_model)

  
  def load_tfidf_model(self, filename):
    """Load generated TFIDF model.

    Args:
        filename (str): file to load data from.

    Returns:
        model (sklearn.feature_extraction.text.TfidfVectorizer): TFIDF model
    """
    with open(filename, 'rb') as model:
      tfidf_model = pickle.load(model)
    
    return tfidf_model
  

  def build_model(self, corpus):
    """Build the TFIDF model with corpus for keyword extraction.

    Args:
        corpus (list): list of documents

    Returns:
        model (sklearn.feature_extraction.text.TfidfVectorizer): TFIDF model
    """
    tfidf_vectorizer = TfidfVectorizer()
    word_count_matrix = tfidf_vectorizer.fit_transform(corpus)

    return tfidf_vectorizer
  

  def initialize_model(self, filename):
    """Initialize the TFIDF model from the data and save it for keyword extraction.

    Args:
        filename (str): name of file to save model to
    """
    data = keyword_extractor.load_data()
    corpus = keyword_extractor.prepare_corpus(data)
    clean_data = keyword_extractor.replace_non_alnum(corpus)
    nouns = keyword_extractor.convert_to_nouns(clean_data)
    tfidf_model = keyword_extractor.build_model(nouns)
    keyword_extractor.save_tfidf_model(filename, tfidf_model)


  def extract_keywords(self, tfidf_vectorizer, document, top_n):
    """Extract keywords for single document.

    Args:
        tfidf_vectorizer (sklearn.feature_extraction.text.TfidfVectorizer): TFIDF model
        document (str): document to extract keywords from
        top_n (int): number of keywords to return

    Returns:
        list: list of keywords extracted from the document
    """
    feature_array = np.array(tfidf_vectorizer.get_feature_names_out())
    doc = tfidf_vectorizer.transform(document)
    tfidf_sorting = np.argsort(doc.toarray()).flatten()[::-1]
    keywords = feature_array[tfidf_sorting][:top_n]
  
    return list(keywords)


if __name__ == "__main__":
  keyword_extractor = KeywordExtractor("path_to_json_file")
  if not os.path.isfile("path_to_saved_tfidf_model"):
    print("Initializing model...")
    keyword_extractor.initialize_model("filename_tfidf_model")
  else:
    print("Loading model and extracting keywords...")
    tfidf_model = keyword_extractor.load_tfidf_model("filename_tfidf_model")
    test_doc = keyword_extractor.lemmatize_document("document_string")
    test_nouns = keyword_extractor.convert_to_nouns([test_doc])
    keywords = keyword_extractor.extract_keywords(tfidf_model, test_nouns, 5)
    print(keywords)
