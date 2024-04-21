import pandas as pd
import numpy as np
import tez
from sklearn import model_selection, preprocessing
import torch
import torch.nn as nn


class RecommenderModel(tez.Model):
    def __init__(self, num_users, num_country, lr=1e-3):
        super().__init__()

        self.learning_rate = lr
        self.user_embed = nn.Embedding(num_users, 16)   
        self.country_embed = nn.Embedding(num_country, 16)
        
        self.hidden = nn.Linear(32, 32)
        self.out = nn.Linear(32, 1)
        self.relu = nn.ReLU()
        self.step_scheduler_after = 'epoch'

    def moniter_metrics(self, outputs, targets):
        outputs = outputs.cpu().detach().numpy()
        targets = targets.cpu().detach().numpy()
        return {'rmse': np.sqrt(((outputs - targets) ** 2).mean())}

    def forward(self, user, country, rating):
        user = self.user_embed(user)
        country = self.country_embed(country)
        out = torch.cat([user, country], 1)
        #out = self.hidden(out)
        #out = self.relu(out)
        out = self.out(out)

        loss = nn.MSELoss()(out, rating.view(-1, 1))
        cal_metrics = self.moniter_metrics(out, rating.view(-1, 1))

        return out, loss, cal_metrics
    
    def fetch_optimizer(self):
        return torch.optim.Adam(self.parameters(), lr=self.learning_rate)
    
    def fetch_scheduler(self):
        return torch.optim.lr_scheduler.StepLR(self.optimizer, step_size=3, gamma=0.7)


class Dataset:
    def __init__(self, user, country, rating):
        self.user = user
        self.country = country
        self.rating = rating
    
    def __len__(self):
        return len(self.user)
    
    def __getitem__(self, item):
        return {
            'user': torch.tensor(self.user[item], dtype=torch.long),
            'country': torch.tensor(self.country[item], dtype=torch.long),
            'rating': torch.tensor(self.rating[item], dtype=torch.float)
        }


def train_NN(dataset_name, model_name):
    
    df = pd.read_csv(dataset_name)

    # df = df.dropna()
    # df = df[['userId', 'movieId', 'rating']]

    # df.columns = ['user', 'country', 'rating']

    lbl_user = preprocessing.LabelEncoder()
    lbl_country = preprocessing.LabelEncoder()

    df.user = lbl_user.fit_transform(df.user.values)
    df.country = lbl_country.fit_transform(df.country.values)

    train_df, test_df = model_selection.train_test_split(df, test_size=0.2, random_state=42, stratify=df.rating.values)

    train_dataset = Dataset(user=train_df.user.values, country=train_df.country.values, rating=train_df.rating.values)

    test_dataset = Dataset(user=test_df.user.values, country=test_df.country.values, rating=test_df.rating.values)

    #es = EarlyStopping(monitor="valid_loss", model_path="model.bin")

    model = RecommenderModel(num_users=len(lbl_user.classes_), num_country=len(lbl_country.classes_), lr=1e-3)
    model.fit(train_dataset, test_dataset, train_bs=1000, valid_bs=1000, fp16=False, epochs=20)

    print('model trained')

    input('press any key to save the model')

    model.save(model_name)

if __name__ == "__main__":
    train_NN(dataset_name='rating.csv', model_name='CF_Neural_Model2.3.bin')