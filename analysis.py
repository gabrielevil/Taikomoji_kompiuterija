import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

class NormalityAnalysis:
    def __init__(self, sample_keys, data, celltype):
        self.sample_keys = sample_keys
        self.data = data
        self.celltype = celltype

    def subset_data(self, celltype, smoking_status):
        subset_keys = self.sample_keys[(self.sample_keys['celltype'] == celltype) &
                                       (self.sample_keys['smoking'] == smoking_status)]
        return subset_keys

    def calculate_means(self):
        smokers_keys = self.subset_data(self.celltype, 'smoker')
        smokers_count = smokers_keys.shape[0]
        smokers = self.data.loc[:, smokers_keys.index]
        smoker_means = smokers.mean(axis=1)

        return smoker_means, smokers_count

    def create_mean_dataframe(self, smoker_means):
        ns_s_means = pd.DataFrame({'mean_smoker': smoker_means})
        return ns_s_means

    def plot_qqnorm(self, smoker_means):
        stats.probplot(smoker_means, dist="norm", plot=plt)
        plt.title('Normality test')
        plt.show()

    def analyze(self):
        smoker_means, smokers_count = self.calculate_means()
        ns_s_means = self.create_mean_dataframe(smoker_means)
        self.plot_qqnorm(ns_s_means['mean_smoker'])

