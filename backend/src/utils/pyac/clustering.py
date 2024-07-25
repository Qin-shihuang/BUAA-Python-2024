import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster

def clustering(fileIds, matrix):
    distance_matrix = [[m[3] for m in matrix[i]] for i in range(len(matrix))]
    linked = linkage(np.array(np.triu_indices(len(distance_matrix), k=1)), method='single')
    cluster_labels = fcluster(linked, t=3, criterion='maxclust')
    # cluster_labels = {i: [] for i in range(1, max(cluster_labels) + 1)}
    clusters = {}
    for i in range(len(cluster_labels)):
        if cluster_labels[i] not in clusters:
            clusters[cluster_labels[i]] = []
        clusters[cluster_labels[i]].append(fileIds[i])
    return clusters
