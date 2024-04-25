from PopularityRecommender import PopularityRecommender
from CollaborativeRecommender import CollaborativeRecommender
from ContentRecommender import ContentBaseRecommender
import pandas as pd

class HybridRecommender:
    def __init__(self, popularity_model: PopularityRecommender=None,
                collaborative_model: CollaborativeRecommender=None,
                content_model: ContentBaseRecommender=None,
                popular_weight: float=0.2, collab_weight: float=0.5, content_weight: float=0.4):
        
        self.popularity_model = popularity_model
        self.collaborative_model = collaborative_model
        self.content_model = content_model
        self.alpha = popular_weight
        self.beta = collab_weight
        self.gamma = content_weight

    def recommend(self, top_n=222):

        if self.popularity_model is not None:
            popularity_recs = self.popularity_model.recommend()

        if self.collaborative_model is not None:
            collaborative_recs = self.collaborative_model.recommend()

        if self.content_model is not None:
            content_recs = self.content_model.recommend()


        if self.content_model is None:
            recommendations = pd.merge(popularity_recs, collaborative_recs, on=('ID', 'Country'), how='outer')
            print(recommendations, self.alpha, self.beta)


            recommendations['Score'] = recommendations['Popularity'] * self.alpha + recommendations['Rating'] * self.beta
                
        elif self.collaborative_model is None:
            recommendations = list(set(popularity_recs + content_recs))

            recommendations['Score'] = recommendations['Popularity'] * self.alpha + recommendations['Similarity'] * self.gamma
                
        else:
            recommendations = list(set(popularity_recs + collaborative_recs + content_recs))

            recommendations['Score'] = recommendations['Popularity']*self.alpha + recommendations['Rating']*self.beta + recommendations['Similarity']*self.gamma


        # recommendations.sort(key=lambda x: scores[x], reverse=True)

        return recommendations[['ID', 'Country', 'Score']][:top_n]
    

if __name__ == '__main__':
    cr, pr = CollaborativeRecommender(user=0, model_name='CF_Neural_Model3.7.bin'), PopularityRecommender()

    hr = HybridRecommender(collaborative_model=cr, popularity_model=pr, popular_weight=0.2, collab_weight=0.8)
    print(hr.recommend())
