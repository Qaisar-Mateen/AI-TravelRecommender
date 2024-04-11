import pandas as pd
import numpy as np


class PopularityRecommender():
    def __init__(self, dataset):
        self.dataset = pd.read_csv(dataset)
        self.alpha = 0.5
        self.beta = 1

