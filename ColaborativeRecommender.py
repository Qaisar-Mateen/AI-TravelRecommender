import pandas as pd
import numpy as np
import tez
from sklearn import model_selection, preprocessing
import torch
import torch.nn as nn

# class CollaborativeRecommender:
#     def __init__(self, data):
#         self.data = data

train_df, test_df = None, None

class RecommenderModel(tez.Model):
    def __init__(self, num_users, num_country):
        super().__init__()

        self.user_embed = nn.Embedding(num_users, 32)
        self.country_embed = nn.Embedding(num_country, 32)
        self.out = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()
        self.step_scheduler_after = 'epoch'

    def moniterMetrics(self, outputs, targets):
        outputs = outputs.cpu().detach().numpy()
        targets = targets.cpu().detach().numpy()
        return {'rmse': np.sqrt(((outputs - targets) ** 2).mean())}

    def forward(self, user, country, rating):
        user = self.user_embed(user)
        country = self.country_embed(country)
        out = torch.cat([user, country], 1)
        out = self.out(out)
        out = self.sigmoid(out)

        loss = nn.MSELoss()(out, rating.view(-1, 1))
        metrics = self.moniterMetrics(out, rating.view(-1, 1))

        return out, loss, metrics
    
    def fetchOptimizer(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)
    
    def fetchScheduler(self):
        return torch.optim.lr_scheduler.StepLR(self.optimizer, step_size=5, gamma=0.1)


def train():
    global train_df, test_df
    df = pd.DataFrame('ratings.csv')

    lbl_user = preprocessing.LabelEncoder()
    lbl_country = preprocessing.LabelEncoder()

    df['user'] = lbl_user.fit_transform(df['user'])
    df['country'] = lbl_country.fit_transform(df['country'])

    train_df, test_df = model_selection.train_test_split(df, test_size=0.2, random_state=42, stratify=df['rating'])

    model = RecommenderModel(num_users=df['user'].nunique(), num_country=df['country'].nunique())

    model.fit(train_df, test_df, train_bs=1024, valid_bs=1024, fp16=True)

    if __name__ == "__main__":
        train()