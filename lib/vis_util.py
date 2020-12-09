from itertools import cycle
from sklearn.metrics import silhouette_score, silhouette_samples
import numpy as np
import matplotlib.pyplot as plt

def plot_PCA_2D(data, target, target_names=None, **kwargs):
    """
    Plots the explained variance of two principal components of a multidimensional dataset. 

    data: PCA features to plot
    target: labels for targets
    target_names: Names to assign the clusters of colors
    """
    if target_names==None:
        target_names = [f'Topic {str(i)}' for i in range(len(set(target)))]
    colors = cycle(['r','g','b','c','m','y','orange','w','aqua','yellow'])
    target_ids = range(len(target_names))
    plt.figure(figsize=(10,10))
    for i, c, label in zip(target_ids, colors, target_names):
        plt.scatter(data[target == i, 0], data[target == i, 1],
                   c=c, label=label, edgecolors='gray', **kwargs)
    plt.legend(bbox_to_anchor=(1,1))

def show_topics(vocab, topic_indexes, topic_labels=None):
    """
    Helper function to show topics from the pyspark LDA results
    args:
        vocab (list): list of all words in the vectorized vocabulary
        topic_indexes (list): indexes of words associated with topics from LDA
        topic_labels (list): labeled topic names.  Naively matches topics with 
            number of topics. i.e. topic 1, topic 2... topic n
    """
    if not topic_labels:
        topic_labels = [f"Topic: {str(i)}" for i in range(len(topic_indexes))]
        assert len(topic_labels) == len(topic_indexes)

    for label, words in zip(topic_labels, topic_indexes):
        topic_words = ", ".join([vocab[word_idx] for word_idx in words])
        print(label + " " + topic_words)


def display_topics(model, feature_names, no_top_words, topic_names=None, show_weights=False):
    """
    Displays Top words associated with topics from Topic Modeling

    model: trained NLP Model (SVD, NMF)
    feature_names: feature names from vectorizers
    no_top_words: number of words to show
    topic_names: List of topic names to assign topics
    show_weights: True to show weights of important words. 
    """
    for ix, topic in enumerate(model.components_):
        if not topic_names or not topic_names[ix]:
            print("\nTopic ", ix)
        else:
            print("\nTopic: '",topic_names[ix],"'")
        if show_weights:
            print([(feature_names[i], topic[i].round(5)) for i in topic.argsort()[:-no_top_words - 1:-1]])
        
        else:
            print(", ".join([feature_names[i]
                            for i in topic.argsort()[:-no_top_words - 1:-1]]))

def plot_silhouette(X, clusters, **kwargs):
    """
    Code adapted from https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_silhouette_analysis.html
    Re-written for plotting scores given data and cluster labels
    args: 
        X (matrix): Features
        clusters (list): labels for each feature topic
    """

    fig = plt.figure(figsize=(15,8))
    s_score = silhouette_score(X, clusters, **kwargs)
    print(f'The average silhouette score is {s_score}')

    all_scores = silhouette_samples(X, clusters, **kwargs)
    n_clusters = set(clusters)

    y_lower = 10
    for cluster in n_clusters:
        # iterate through clusters
        # get scores from current cluster
        current_cluster_silhouette_scores = all_scores[clusters==cluster]

        current_cluster_silhouette_scores.sort()

        size_current_cluster = current_cluster_silhouette_scores.shape[0]
        # set boundaries for plotting new bars
        y_upper = y_lower + size_current_cluster 

        plt.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            current_cluster_silhouette_scores,
            )
        plt.text(-0.05, y_lower + 0.5*size_current_cluster, str(cluster))

        y_lower = y_upper + 10
    # plot average sihlouette scores    
    plt.vlines(x=s_score, ymin=10, ymax=y_upper, linestyles='--', color='r')
    
from scipy.cluster.hierarchy import dendrogram

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)
