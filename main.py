from load import RDSReader
from control import QualityControl

def main():
    #Load data from inputs directory
    reader = RDSReader()

    #Read data into a DataFrame
    samplekey_df = reader.read_to_dataframe("./inputs/samplekey2.rds")
    print("Samplekey:\n", samplekey_df.head())

    genomemap_df = reader.read_to_dataframe("./inputs/genomemap2.rds")
    print("Genomemap:\n", genomemap_df.head())

    #Read data into a matrix
    data_matrix = reader.read_to_matrix("./inputs/data2.rds")
    print("Data:\n", data_matrix)

    #Perform quality control on data
    qc = QualityControl(data_matrix, genomemap_df)
    qc.calculate_mean_modifications()
    #Plot the results of qc
    qc.plot_modification_levels()


if __name__ == '__main__':
    main()

