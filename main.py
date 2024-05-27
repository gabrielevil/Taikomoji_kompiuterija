from load import RDSReader
from control import QualityControl
from ttest import TTestHandler
from corrPlot import CorrelationPlot
from analysis import NormalityAnalysis
import pandas as pd
import sys

def main():
    #Check if number of arguments is correct
    if len(sys.argv) != 4:
        print("Usage: python main.py <dna_methylation_matrix> <genome_map> <sample_key>")
        sys.exit(1)

    _, dna_methylation, genome_map, sample_key = sys.argv   
    #Load data from ARGV
    reader = RDSReader()

    #Read data into a DataFrame
    samplekey_df = reader.read_to_dataframe(sample_key)
    print("Samplekey:\n", samplekey_df.head())

    genomemap_df = reader.read_to_dataframe(genome_map)
    print("Genomemap:\n", genomemap_df.head())

    #Read data into a matrix
    data_matrix = reader.read_to_matrix(dna_methylation)
    print("Data:\n", data_matrix)

    #Perform quality control on data
    qc = QualityControl(data_matrix, genomemap_df)
    qc.calculate_mean_modifications()
    #Plot the results of qc
    qc.plot_modification_levels()

    # Perform t-test
    t_test = TTestHandler(samplekey_df, data_matrix, "bcell", 43)
    t_test.perform_t_tests()
    # Plot t-test results
    t_test.plot_p_values()
    t_test.plot_mean_diff()
    t_test.plot_volcano()

    #Correlation heatmap
    correlation_plot = CorrelationPlot(data_matrix)
    correlation_plot.calculate_correlation_matrix()
    correlation_plot.plot_correlation()

    correlation_plot.hierarchical_clustering()

    #Normality test
    data_df = pd.DataFrame(data_matrix, columns=samplekey_df.index)
    smoking_analysis = NormalityAnalysis(samplekey_df, data_df, "tcd8")
    smoking_analysis.analyze()

if __name__ == '__main__':
    main()
