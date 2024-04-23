from PopularityRecommender import PopularityRecommender
from CollaborativeRecommender import CollaborativeRecommender
from ContentRecommender import ContentBaseRecommender

class HybridRecommender:
    def __init__(self, popularity_model: PopularityRecommender=None,
                collaborative_model: CollaborativeRecommender=None,
                content_model: ContentBaseRecommender=None,
                alpha: float=0.3, beta: float=0.3, gamma: float=0.4):
        
        self.popularity_model = popularity_model
        self.collaborative_model = collaborative_model
        self.content_model = content_model
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def recommend(self, top_n=222):

        if self.popularity_model is not None:
            popularity_recs = self.popularity_model.recommend()

        if self.collaborative_model is not None:
            collaborative_recs = self.collaborative_model.recommend()

        if self.content_model is not None:
            content_recs = self.content_model.recommend()

        scores = {}

        if self.content_model is None:
            recommendations = list(set(collaborative_recs + popularity_recs))
                        
            for rec in recommendations:
                scores[rec] = (self.alpha * (rec in popularity_recs) +
                            self.beta * (rec in collaborative_recs))
                
        elif self.collaborative_model is None:
            recommendations = list(set(popularity_recs + content_recs))

            for rec in recommendations:
                scores[rec] = (self.alpha * (rec in popularity_recs) +
                            self.gamma * (rec in content_recs))
                
        else:
            recommendations = list(set(popularity_recs + collaborative_recs + content_recs))

            for rec in recommendations:
                scores[rec] = (self.alpha * (rec in popularity_recs) +
                            self.beta * (rec in collaborative_recs) +
                            self.gamma * (rec in content_recs))


        recommendations.sort(key=lambda x: scores[x], reverse=True)

        return recommendations[:top_n]