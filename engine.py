# Import all the cool stuff that makes stuff look cool... oh, and the 'sciency' stuff...
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sqlalchemy import create_engine
import pymysql

engine = create_engine("mysql+pymysql://clfys5mqr32m42ct:p88c2ksec0jals84@rtzsaka6vivj2zp1.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/uyoymimfmvofh7fq")
query = "SELECT * FROM moovees"

# The 'stars' of the show - the movies themselves!
movies = pd.read_sql_query(query, engine)
# Break up the big genre string into a string array
movies['genres'] = movies['genres'].str.split('|')
# Convert genres to string value
movies['genres'] = movies['genres'].fillna("").astype('str')

# CONVERTS THE MOVIE GENRES INTO A MATRIX OF TF-IDF FEATURES AND FORMATS THE DATA FOR THE COSINE SIMILARITY ALGORYTHM
tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(movies['genres'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)





