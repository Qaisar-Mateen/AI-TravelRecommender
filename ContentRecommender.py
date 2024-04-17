# import pandas as pd
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity


# data = pd.read_csv('world-countries.csv')

# print(data)

# print('processing data...')

# def merge_keywords(row):
#     row['keywords'] = str(row['keywords']) + ' ' + str(row['climate'])
#     return row

# data = data.apply(merge_keywords, axis=1)
# data.drop('climate', axis=1, inplace=True)

# data = data.drop_duplicates(subset='country')    

# print(data)

# country = input('Enter a country you like: ')
# budget = int(input('Enter your budget: '))

# like_df = data[data['country'].str.lower() == country.lower()]
# if like_df.empty:
#     print('Country not found')
#     exit(0)

# print(like_df)

# print('vectorizing data...')

# tf_idf = TfidfVectorizer(stop_words='english')

# tf_idf_matrix = tf_idf.fit_transform(data['keywords'])

# vec = CountVectorizer(stop_words='english')
# vec_matrix = vec.fit_transform(data['keywords'])

# print('calculating similarity...')

# cosine_sim = cosine_similarity(tf_idf_matrix, tf_idf_matrix)
# sim = cosine_similarity(vec_matrix, vec_matrix)

# def recomender(country, budget, num_of_rec=5):
#     print('recommending...')

#     global data, cosine_sim, sim
#     idx = data[data['country'].str.lower() == country.lower()].index[0]
#     sim_scores = list(enumerate(cosine_sim[idx]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     #sim_scores = sim_scores[:6]
#     country_indices = [i[0] for i in sim_scores]
#     print("\n\nTF-IDF Scores:\n")
    
#     reced = 0
#     recommend1 = pd.DataFrame(columns=['Country', 'Cost Per Day', 'Score'])
#     for index, score in zip(country_indices, sim_scores):
#         if data['country'].iloc[index].lower() != country.lower() and data['avg cost per day'].iloc[index] <= budget+5:
#             recommend1 = recommend1._append({'Country': data['country'].iloc[index], 
#                                                   'Cost Per Day': data['avg cost per day'].iloc[index], 
#                                                   'Score': score[1]}, ignore_index=True)
#             reced += 1
#             if reced == num_of_rec:
#                 break
#     print(recommend1)

#     idx = data[data['country'].str.lower() == country.lower()].index[0]
#     sim_scores = list(enumerate(sim[idx]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     #sim_scores = sim_scores[:6]
#     country_indices = [i[0] for i in sim_scores]
#     print("\n\nCount Vectorizer Scores:\n")
    
#     reced = 0
#     recommend2 = pd.DataFrame(columns=['Country', 'Cost Per Day', 'Score'])
#     for index, score in zip(country_indices, sim_scores):
#         if data['country'].iloc[index].lower() != country.lower() and data['avg cost per day'].iloc[index] <= budget+5:
#             print(data['country'].iloc[index], data['avg cost per day'].iloc[index], score[1])
#             recommend2 = recommend2._append({'Country': data['country'].iloc[index], 
#                                                   'Cost Per Day': data['avg cost per day'].iloc[index], 
#                                                   'Score': score[1]}, ignore_index=True)
#             reced += 1
#             if reced == num_of_rec:
#                 break

#     print(recommend2)

# recomender(country, budget)

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from time import sleep as s
import warnings
from gensim import models, similarities

warnings.simplefilter(action='ignore', category=FutureWarning)

class ContentBaseRecommender:

    def __init__(self, data_file='world-countries.csv', wait_time=0.1):
        self.data = pd.read_csv(data_file)
        self.wait = wait_time
        self.data = self.process_data(self.data)
        print(self.data)

        print('performing vectorization...')
        s(self.wait)
        
        self.tf_idf = TfidfVectorizer(stop_words='english')
        self.vec = CountVectorizer(stop_words='english')
        
        self.tf_idf_matrix = self.tf_idf.fit_transform(self.data['keywords'])
        self.vec_matrix = self.vec.fit_transform(self.data['keywords'])

        print('calculating similarity...')
        s(self.wait)
 
        self.cosine_sim = cosine_similarity(self.tf_idf_matrix, self.tf_idf_matrix)
        self.sim = cosine_similarity(self.vec_matrix, self.vec_matrix)


    def process_data(self, data):
        
        print('processing data...')
        s(self.wait)
        data['keywords'] = data.apply(lambda row: str(row['keywords']) + ' ' + str(row['climate']), axis=1)
        data.drop('climate', axis=1, inplace=True)
        data = data.drop_duplicates(subset='country')
        data['keywords'] = data['keywords'].str.replace(r'\s+', ' ')

        print('data processed')
        s(self.wait)
        return data


    def get_TF_IDF_recomendation(self, country, budget, num_of_rec=5):

        idx = self.data[self.data['country'].str.lower() == country.lower()].index[0] -1
        
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        country_indices = [i[0] for i in sim_scores]

        reced = 0
        recommendation = pd.DataFrame(columns=['Country', 'Cost Per Day', 'Score'])
        
        for index, score in zip(country_indices, sim_scores):
            if self.data['country'].iloc[index].lower() != country.lower() and self.data['avg cost per day'].iloc[index] <= budget+5:
                recommendation = recommendation._append({'Country': self.data['country'].iloc[index], 
                                                  'Cost Per Day': self.data['avg cost per day'].iloc[index], 
                                                  'Score': score[1]}, ignore_index=True)
                reced += 1
        
                if reced == num_of_rec:
                    break
        
        return recommendation


    def get_CountVectorizer_recomendation(self, country, budget, num_of_rec=5):
        
        idx = self.data[self.data['country'].str.lower() == country.lower()].index[0] -1
        sim_scores = list(enumerate(self.sim[idx]))

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        print('score: ',sim_scores)

        country_indices = [i[0] for i in sim_scores]

        reced = 0
        recommendation = pd.DataFrame(columns=['Country', 'Cost Per Day', 'Score'])
        
        for index, score in zip(country_indices, sim_scores):
            if self.data['country'].iloc[index].lower() != country.lower() and self.data['avg cost per day'].iloc[index] <= budget+5:
                recommendation = recommendation._append({'Country': self.data['country'].iloc[index], 
                                                  'Cost Per Day': self.data['avg cost per day'].iloc[index], 
                                                  'Score': score[1]}, ignore_index=True)
                reced += 1
        
                if reced == num_of_rec:
                    break
        
        return recommendation
    

    def recommend(self, country, budget, num_of_rec=5, tf_idf=True, count_vectorizer=True):

        like_df = self.data[self.data['country'].str.lower() == country.lower()]
        
        if like_df.empty:
            print('Country not found')
            exit(0)
        print(like_df)

        print('generating recommendations...')
        s(self.wait)
        
        if tf_idf:
            print('\n\nTF-IDF Score Recomendation:\n')
            print(self.get_TF_IDF_recomendation(country, budget, num_of_rec))

        if count_vectorizer:
            print('\n\nCount Vectorizer Score Recomendation:\n')
            print(self.get_TF_IDF_recomendation(country, budget, num_of_rec))


if __name__ == '__main__':
    recommender = ContentBaseRecommender('world-countries.csv', .5)
    country = input('Enter a country you like: ')
    budget = int(input('Enter your budget: '))
    recommender.recommend(country, budget, 5, tf_idf=True, count_vectorizer=True)