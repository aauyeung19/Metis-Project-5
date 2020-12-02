"""
Recommendation Code for returning similar articles to a Query
"""

from nlp import NLPPipe
from gensim.models.doc2vec import Doc2Vec
import pandas as pd
import numpy as np

# Get Query 
# Predict Topic Probability
# Use NLP to Predict Topic Distribution
# Map Topic Distribution to Topic Cluster based On Probability Distribution
# -- Maybe Look at Cosine Similarity?
# 
