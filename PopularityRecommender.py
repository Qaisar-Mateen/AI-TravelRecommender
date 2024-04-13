import pandas as pd
import numpy as np


class PopularityRecommender():
    def __init__(self, dataset='world-popularity.csv', alpha=0.5, beta=0.5):
        self.dataset = pd.read_csv(dataset)
        self.alpha = alpha
        self.beta = beta

    def UpdateWeights(self, a, b):
        self.alpha = a
        self.beta = b
    
    def CalculatePopularity(self):
        """
            Popularity Formula:
            Popularity = ((alpha * Popularity Index) * (beta * Avg Visitors) / mean(Popularity Index))/ Max Popularity
        """

        def CalculatePopularityScore(row):

            a = (row['Popularity Index'])*(row['Avg Visitors'])
            a += row['Popularity Index']*self.alpha
            a += row['Avg Visitors']*self.beta 
            a /= np.mean(self.dataset['Popularity Index'])

            return a
        
        self.dataset['Popularity'] = self.dataset.apply(CalculatePopularityScore, axis=1)

        def NormalizePopularity(row):
            return row['Popularity'] / np.max(self.dataset['Popularity'])
        
        self.dataset['Popularity'] = self.dataset.apply(NormalizePopularity, axis=1)

    def Recommend(self):
        self.CalculatePopularity()
        
        print('Popularity mean: ', np.mean(self.dataset['Popularity']))
        print('popularity max, min: ', np.max(self.dataset['Popularity']), np.min(self.dataset['Popularity']))
        
        return self.dataset


if __name__ == '__main__':
    PR = PopularityRecommender('world-popularity.csv', alpha=0.7, beta=0.1)
    print(PR.Recommend())