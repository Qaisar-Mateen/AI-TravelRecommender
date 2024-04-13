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
