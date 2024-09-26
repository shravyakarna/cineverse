import numpy as np
import matplotlib as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle
data = pd.read_csv('moviedata.csv',sep='|')
data.rename(columns={'Unnamed:0': 'id'}, inplace=True)
columns={'maincast','directors','genres','title','plotsummary'}
#these fields, once cleaned, will be the basis for the cosine similarity matrix
def relevant(data):
    relevant_features=[]
    for i in range(0,data.shape[0]):
        relevant_features.append(data['title'][i]+''+data['directors'][i]+''+data['genres'][i]+''+data['plotsummary'][i]+' '+data['maincast'][i])
    return relevant_features
data['relevant_features']=relevant(data)
tfidf=TfidfVectorizer(stop_words='english')
#filler words like 'or','and','to' etc are cleaned out, leaving only keywords
tfidf_matrix = tfidf.fit_transform(data['relevant_features'])
tfidf_matrix.shape
#defining the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix,tfidf_matrix)
print(cosine_sim)
indices = pd.Series(data.index, index=data['title']).drop_duplicates()
#indices['Stillwater']
#sim_scores = list(enumerate(cosine_sim[indices['Stillwater']]))
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 5 most similar movies
    movies=data['title'].iloc[movie_indices]
    ratings=data['rating'].iloc[movie_indices]
    dict={"Movies":movies, "IMDB Rating":ratings}
    final_df=pd.DataFrame(dict)
    final_df.reset_index(drop=True,inplace=True)
    final_df = final_df.sort_values(by='IMDB Rating', ascending=False)
    return final_df
print(get_recommendations('Inception'))