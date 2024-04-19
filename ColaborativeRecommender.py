import pandas as pd
import numpy as np
import tez
from sklearn import model_selection
import torch
import torch.nn as nn

# class CollaborativeRecommender:
#     def __init__(self, data):
#         self.data = data

train_df, test_df = None, None

def train():
    global train_df, test_df
    df = pd.DataFrame('ratings.csv')

    train_df, test_df = model_selection.train_test_split(df, test_size=0.2, random_state=42, stratify=df['rating'])