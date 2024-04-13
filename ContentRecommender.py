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

warnings.simplefilter(action='ignore', category=FutureWarning)
