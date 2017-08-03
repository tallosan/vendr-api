#
# @author :: Andrew Tallos
# Collaborative Filtering algorithm for the Vendr Recommendation System.
#
# ==========================================================================


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class Recommender(object):

    ''' Create a Recommender for a set of users. '''
    def __init__(self, users):
        self.features = self.create_matrix(users)

    ''' Create a matrix of feature vectors for each user.
        Args:
            users -- A set of arrays, each containing a given user's activity.
    '''
    def create_matrix(self, users):
        
        features = []
        for user in users:
            features.append(user.activity)

        return features

    def recommend_to(self, user_i):

        # Get a set of recommenders.
        print self.features[user_i]
        recommenders = self.find_recommenders(user_i)
        sparse_features = [
                                list(self.features[user_i]).index(sf)
                                for sf in self.features[user_i] if sf == 0
        ]
        print sparse_features
        print recommenders
        for recommender in recommenders:
            pass
   
    ''' Make a recommendation to a given user.
        Args:
            user_i -- The index of the user in our features matrix.
    '''
    def find_recommenders(self, user_i):
        
        target_user = self.features[user_i]
        
        # Get the similarity for each user.
        sims = []
        for _user in range(len(self.features)):
            if _user != user_i:
                user = self.features[_user]
                sims.append([_user, self.get_similarity(target_user, user)])
        
        sims.sort(key=lambda v: v[1], reverse=True)
        indices = [s[0] for s in sims[:2]]
        
        return [self.features[recommender_i] for recommender_i in indices]


    ''' Calculate the similarity between two vectors. N.B. -- This is really
        just a wrapper for whatever algorithm we choose. '''
    def get_similarity(self, target, vector):

        return self.cosine_similarity(target, vector)
    
    ''' Calculate the cosine simliarity. '''
    def cosine_similarity(self, target, vector):
        
        return cosine_similarity(self.normalize(target), self.normalize(vector))
    
    ''' Normalize a feature vector. We'll use mean subtraction.
        Args:
            vector -- The vector to normalize.
    '''
    def normalize(self, vector):

        mean = np.mean(vector)
        return vector - mean
 
    def get_recommendations(self):
        pass


class User(object):

    def __init__(self, activity):
        self.activity = activity


u0 = User(np.asarray([1, 0, 0, 2, 3, 1])); u1 = User(np.asarray([2, 0, 1, 1, 4, 2]))
u2 = User(np.asarray([5, 0, 2, 8, 6, 3])); u5 = User(np.asarray([4, 1, 2, 8, 12, 4]))
u3 = User(np.asarray([0, 5, 7, 0, 1, 4])); u4 = User(np.asarray([1, 6, 4, 4, 3, 1]))

users = [u0, u1, u2, u3, u4, u5]
r = Recommender(users)
r.recommend_to(0)

