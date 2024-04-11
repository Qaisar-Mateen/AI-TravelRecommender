import pandas as pd
import numpy as np


class PopularityRecommender():
    def __init__(self, dataset):
        self.dataset = pd.read_csv(dataset)
        self.alpha = 0.5
        self.beta = 1

    def UpdateWeights(self, a, b):
        self.alpha = a
        self.beta = b
    
    def CalculatePopularity(self):

        def CalculatePopularityScore(row):
            a = (self.alpha * row['Popularity Index'])*(self.beta * row['Avg Visitors'])
            a /= np.mean(self.dataset['Popularity Index'])
            return a
        
        self.dataset['Popularity'] = self.dataset.apply(CalculatePopularityScore, axis=1)
