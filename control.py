import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class QualityControl:
    def __init__ (self, modification_matrix, genomemap):
        self.mod_matrix = modification_matrix
        self.genomemap = genomemap
        self.combined_data = None

    def calculate_mean_modifications(self):
        mean_modifications = np.mean(self.mod_matrix, axis=1)  
        mean_df = pd.DataFrame(mean_modifications, index=self.genomemap.index, columns=['mean_modification'])       
        self.combined_data = self.genomemap.join(mean_df)

    def compare_modification_levels(self):
        if self.combined_data is None:
            self.calculate_mean_modifications()

        element_means = self.combined_data.groupby('relation_to_island')['mean_modification'].mean()
        element_means = element_means.sort_values()
        return element_means
    
    def plot_modification_levels(self):
        if self.combined_data is None:
            self.calculate_mean_modifications()

        element_means = self.compare_modification_levels()
        element_means.plot(kind='bar', color='skyblue')
        plt.xlabel('Relation to Island')
        plt.ylabel('Average Modification Level')
        plt.title('Average CpG Modification Levels by Relation to Island')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

