import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

def clustering(fileIds, matrix):
    dist_vector = squareform(matrix)
    linked = linkage(dist_vector, method='average', metric='precomputed')
    cluster_labels = fcluster(linked, 0.35, criterion='distance')
    clusters = {}
    for i in range(len(cluster_labels)):
        if cluster_labels[i] not in clusters:
            clusters[int(cluster_labels[i])] = []
        clusters[int(cluster_labels[i])].append(fileIds[i])
    return clusters
