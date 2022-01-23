#!/usr/bin/python3


"""Script for executing the keyword extractor."""


import os
from tf_idf import KeywordExtractor


if __name__ == "__main__":
    keyword_extractor = KeywordExtractor('file_to_cleaned_data')

    if not os.path.isfile('file_to_tfidf_model'):
      print('Initializing model...')
      keyword_extractor.initialize_model('file_to_tfidf_model')
      print('Initialization successful. Start extracting keywords...')
      tfidf_model = keyword_extractor.load_tfidf_model('file_to_tfidf_model')
      keyword_extractor.create_dataframe(tfidf_model)
    
    else:
      print('Loading model and extracting keywords...')
      tfidf_model = keyword_extractor.load_tfidf_model('file_to_tfidf_model')
      keyword_extractor.create_dataframe(tfidf_model)
