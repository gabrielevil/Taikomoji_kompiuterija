import pyreadr
import pandas as pd
import numpy as np

class RDSReader:
    def read_to_dataframe(self, file_path):
        #Reads RDS into a dataframe
        result = pyreadr.read_r(file_path)
        df = result[None]
        return df

    def read_to_matrix(self, file_path):
        #Reads RDS into a numpy matrix
        result = pyreadr.read_r(file_path)
        df = result[None]
        matrix = df.to_numpy()
        return matrix
