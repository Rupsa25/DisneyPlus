import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import warnings
def model(df):
  #model
  warnings.simplefilter(action='ignore', category=FutureWarning)
  tfidf_vectorizer = TfidfVectorizer(stop_words='english')
  tfidf_matrix = tfidf_vectorizer.fit_transform(df['description'])

  # Perform Clustering (K-Means)
  num_clusters = 17  # You can adjust this value
  kmeans = KMeans(n_clusters=num_clusters, random_state=42)
  kmeans.fit(tfidf_matrix)
  return [tfidf_vectorizer,tfidf_matrix,kmeans]


def recommend_movie(df,input_movie):
  description = df[df['title'] == input_movie]['description'].values[0]
  # Find the cluster of the input movie
  [tfidf_vectorizer,tfidf_matrix,kmeans] = model(df)
  input_movie_vector = tfidf_vectorizer.transform([description])
  cluster = kmeans.predict(input_movie_vector)[0]

  # Get movie recommendations from the same cluster
  cluster_center = kmeans.cluster_centers_[cluster]
  closest, _ = pairwise_distances_argmin_min(cluster_center.reshape(1, -1),tfidf_matrix)
  recommendations = df.iloc[closest]
  return recommendations['title'].tolist()[0]

