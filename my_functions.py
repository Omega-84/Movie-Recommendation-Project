import numpy as np
import pandas as pd
import operator
from scipy import spatial
from ast import literal_eval as eval

df = pd.read_csv("movie_data.csv",index_col='id')

for i in ['Genre list','Top actor list','Director list','Genres bin','Actors bin','Director bin']:
    df[i] = df[i].apply(lambda x: eval(x))

def create_movie_dict(dataframe,index):
    """Create a tuple containg specific information about the movie
    Attributes: dataframe - the pandas dataframe containing movie records
    index - the index of movie record
    """
    tup =  (dataframe['title'][index] , dataframe['Genres bin'][index] ,dataframe['Actors bin'][index], dataframe['Director bin'][index], dataframe['popularity'][index])
    return tup


def compute_dist(df1,ind1,df2,ind2):
    """Computes the distance between 2 movies on basis of cosine distance

    Attributes: dataframes and indices    
    """


    mov1 = create_movie_dict(df1,ind1)
    mov2 = create_movie_dict(df2,ind2)
    
    genre_1 = mov1[1]
    genre_2 = mov2[1]
    
    genre_distance = spatial.distance.cosine(genre_1, genre_2)
    
    actor_1 = mov1[2]
    actor_2 = mov2[2]
    
    actor_distance = spatial.distance.cosine(actor_1, actor_2)
    
    dir_1 = mov1[3]
    dir_2 = mov2[3]
    
    dir_distance = spatial.distance.cosine(dir_1, dir_2)
        
    pop_1 =  mov1[4]
    pop_2 =  mov2[4]
    
    popularity_distance = abs(pop_1 - pop_2)
    
    return genre_distance + popularity_distance + actor_distance + dir_distance


def get_recommendations(ID,K=5):
    """This function returns the top 5 recommendations for the given movie along with the genres, cast and director

    Attributes:ID - the index for the movie 
    K - the number of recommendations needed ; default=5
    """
    distances = []
    training = df.drop(ID,axis=0)
    train_movie_dict = dict(zip(training.index,training['title']))
    for key, value in train_movie_dict.items():
        dist = compute_dist(training,key,df,ID)
        distances.append((value, dist,key))
    distances.sort(key=operator.itemgetter(1))
    
    recommendation_list = []
    for i in range(K): 
        name = distances[i][0]
        idd = distances[i][2]
        recommendation_list.append((str( name + ' \n\t ' + " Genre: " + str(df['Genre list'][idd]).strip('[]').replace(' ','') +
             ' \n\t ' + " Actors: "+str(df['Top actor list'][idd]).strip('[]') + 
             ' \n\t ' + " Director(s): "+str(df['Director list'][idd]).strip('[]')),idd))
    return recommendation_list
