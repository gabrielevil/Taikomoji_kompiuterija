from load import RDSReader
from control import QualityControl
from ttest import TTestHandler
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
    #qc = QualityControl(data_matrix, genomemap_df)
    #qc.calculate_mean_modifications()
    #Plot the results of qc
    #qc.plot_modification_levels()

    analyzer = TTestHandler(genomemap_df, samplekey_df, data_matrix)
    analyzer.perform_t_tests()
    analyzer.plot_p_values()
    #analyzer.plot_mean_diff()
    analyzer.plot_volcano()

if __name__ == '__main__':
    main()

