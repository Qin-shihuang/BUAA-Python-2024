import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster

def clustering(fileIds, matrix):
    linked = linkage(np.array(np.triu_indices(len(matrix), k=1)), method='single')
    cluster_labels = fcluster(linked, t=3, criterion='maxclust')
    clusters = {}
    for i in range(len(cluster_labels)):
        if cluster_labels[i] not in clusters:
            clusters[int(cluster_labels[i])] = []
        clusters[int(cluster_labels[i])].append(fileIds[i])
    return clusters
