# Import all the cool stuff that makes stuff look cool... oh, and the 'sciency' stuff...
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sqlalchemy import create_engine
import pymysql

engine = create_engine("mysql+pymysql://clfys5mqr32m42ct:p88c2ksec0jals84@rtzsaka6vivj2zp1.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/uyoymimfmvofh7fq")
query = "SELECT * FROM movies"

# The 'stars' of the show - the movies themselves!
movies = pd.read_sql_query(query, engine)
# Break up the big genre string into a string array
movies['genres'] = movies['genres'].str.split('|')
# Convert genres to string value
movies['genres'] = movies['genres'].fillna("").astype('str')
movies['cast'] = movies['cast'].fillna("").astype('str')
movies['movie_descriptions'] = movies['movie_descriptions'].fillna("").astype('str')

# CONVERTS THE MOVIE GENRES INTO A MATRIX OF TF-IDF FEATURES
tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')

# GENRE PREP
genre_matrix = tf.fit_transform(movies['genres'])
genre_cosine_sim = linear_kernel(genre_matrix, genre_matrix)

# CAST PREP
cast_matrix = tf.fit_transform(movies['cast'])
cast_cosine_sim = linear_kernel(cast_matrix, cast_matrix)

# DESCRIPTION PREP
desc_matrix = tf.fit_transform(movies['movie_descriptions'])
desc_cosine_sim = linear_kernel(desc_matrix, desc_matrix)

