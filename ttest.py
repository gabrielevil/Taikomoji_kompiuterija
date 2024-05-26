from scipy.stats import ttest_ind
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class TTestHandler:
    def __init__(self, genmap, sample, dat):
        self.genmap = genmap
        self.sample = sample
        self.dat = dat
        self.t_test_results = []
        self.p_values = []
        self.mean_differences = []
        self.count = 0

    def perform_t_tests(self):
        # Creating boolean arrays for indexing dat
        condition_high = ((self.sample.iloc[:, 8] > 43) & (self.sample.iloc[:, 4] == "bcell")).to_numpy()
        condition_low = ((self.sample.iloc[:, 8] <= 43) & (self.sample.iloc[:, 4] == "bcell")).to_numpy()

        for i in range(self.dat.shape[0]):  
            group1 = self.dat[i, condition_high]
            group2 = self.dat[i, condition_low]

            if group1.size > 1 and group2.size > 1:
                t_stat, p_value = ttest_ind(group1, group2, alternative="two-sided")

                self.t_test_results.append((t_stat, p_value))
                self.p_values.append(p_value)
                self.mean_differences.append(np.nanmean(group1) - np.nanmean(group2))

                # Count tests with significant p-values
                if p_value <= 0.05:
                    self.count += 1
        print("Count of tests with significant p-values: ", self.count)

    def plot_p_values(self):
        plt.hist(self.p_values, bins=20, color='blue', edgecolor='black')
        plt.title('Histogram of P-values from T-Tests')
        plt.xlabel('P-value')
        plt.ylabel('Frequency')
        plt.show()

    def plot_mean_diff(self):
        plt.hist(self.mean_differences, bins=20, color='blue', edgecolor='black')
        plt.title('Histogram of mean differences from T-Tests')
        plt.xlabel('Mean differences')
        plt.ylabel('Frequency')
        plt.show()

    def plot_volcano(self):
        neg_log_pvals = -np.log10(np.array(self.p_values))

        fold_change_threshold = 0.05
        p_value_threshold = 0.05

        # Color points
        colors = []
        for log_fold_change, p_value in zip(self.mean_differences, neg_log_pvals):
            if log_fold_change > fold_change_threshold and p_value > -np.log10(p_value_threshold):
                colors.append('red')  # Significant and up-regulated
            elif log_fold_change < -fold_change_threshold and p_value > -np.log10(p_value_threshold):
                colors.append('blue')  # Significant and down-regulated
            else:
                colors.append('grey')  # Not significant

        # Create plot
        plt.figure(figsize=(10, 6))
        plt.scatter(self.mean_differences, neg_log_pvals, c=colors, alpha=0.5)
        plt.title('Volcano Plot')
        plt.xlabel('Mean differences')
        plt.ylabel('-Log10 P-value')
        plt.axhline(y=-np.log10(p_value_threshold), color='red', linestyle='dashed')
        plt.axvline(x=fold_change_threshold, color='black', linestyle='dashed')
        plt.axvline(x=-fold_change_threshold, color='black', linestyle='dashed')
        plt.grid(True)
        plt.show()
