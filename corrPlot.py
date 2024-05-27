import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, dendrogram


class CorrelationPlot:
    def __init__(self, data_matrix):
        self.data_matrix = data_matrix

    def calculate_correlation_matrix(self):
        self.cor_matrix = np.corrcoef(self.data_matrix.T)

    def plot_correlation(self):
        plt.figure(figsize=(10, 8))
        sns.set(font_scale=0.8)
        sns.heatmap(self.cor_matrix, cmap='coolwarm_r', annot=True, fmt=".2f", linewidths=0.5)
        plt.title('Correlation before clusterization', fontsize=20, fontweight='bold')
        plt.xlabel('')
        plt.ylabel('')
        plt.xticks(rotation=90, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()

    def hierarchical_clustering(self, title='Correlation after clusterization'):
        abs_cor_matrix = np.abs(self.cor_matrix)
        distance_matrix = 1 - abs_cor_matrix
        sym_distance_matrix = 0.5 * (distance_matrix + distance_matrix.T)
        np.fill_diagonal(sym_distance_matrix, 0)
        linkage_matrix = linkage(squareform(sym_distance_matrix), method='average')
        order = dendrogram(linkage_matrix, no_plot=True)['leaves']
        ordered_cor_matrix = self.cor_matrix[order, :][:, order]

        plt.figure(figsize=(10, 8))
        sns.set(font_scale=0.8)
        sns.heatmap(ordered_cor_matrix, cmap='coolwarm_r', annot=True, fmt=".2f", linewidths=0.5)
        plt.title(title, fontsize=20, fontweight='bold')
        plt.xlabel('')
        plt.ylabel('')
        plt.xticks(rotation=90, ha='left')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()