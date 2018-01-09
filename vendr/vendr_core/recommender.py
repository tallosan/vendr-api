#
# Vendr Recommendation System
#
# We'll use a combination of approaches.
#
# 1. Collaborative filtering.
# 2. Content-Based profiling.
#
# -- t-SNE visualizer: http://lvdmaaten.github.io/tsne/
#
#
# High Level Overview:
#
# The first thing we need to do is maintain our data set. Naturally, it'll
# be dynamic, and as such we'll need to ensure that our model is constantly
# learning from any new input.
#
# For each user, we'll generate recomendations according to a score that we'll
# assign each property. This score will be the sum of two values --
#
#               collaborative_filtering_score + content_profile_score
#
#
#
# Data:
#
# We can create one large feature vector, and share it accross users.
# The vector has size N_loc x N_loc (N_loc^2), where N is the number of properties
# in a given location (loc)
#
# A user needs to keep track of their location in each matrix, represented as a
# standard coordinate -- (i, j).
#
# Note, to avoid having to generate new user coordinates upon a new matrix entry,
# we can simply ensure that all new property entries are appended to the end
# of the matrix, i.e. -- the row will end up at the bottom of the matrix, the
# column at the farthest right.
#
# Layout:
#
# Each row corresponds to a given user, and each column to a given property.
# Each feature vector in our matrix is a representation of a user, and their
# interpretation of our properties.
#
# -- Each i, j entry is the preferance score given by user `i` to a property `j`.
#
# Content-Based profiling
#
# Cosine Similarity.
# 
