'''
Name: Olivia Fang
'''

from binary_perceptron import BinaryPerceptron # Your implementation of binary perceptron
from plot_bp import PlotBinaryPerceptron
import csv  # For loading data.
from matplotlib import pyplot as plt  # For creating plots.
from remapper import remap

class PlotRingBP(PlotBinaryPerceptron):
    """
    Plots the Binary Perceptron after training it on the ring dataset
    ---
    Extends the class PlotBinaryPerceptron
    """

    def __init__(self, bp, plot_all=True, map = False, n_epochs=25):
        self.IS_REMAPPED = map
        super().__init__(bp, plot_all, n_epochs) # Calls the constructor of the super class

    def read_data(self):
        """
        Read data from the ring dataset
        ---
        Overrides the method in PlotBinaryPerceptron
        """
        data_as_strings = list(csv.reader(open('ring-data.csv'), delimiter=','))
        # Hidden to protect information

    def plot(self):
        """
        Plots the dataset as well as the binary classifier
        ---
        Overrides the method in PlotBinaryPreceptron
        """
        plt.title("Ring Data Perceptron Training Plot")
        plt.xlabel("Angle")
        plt.ylabel("Radius")
        plt.legend(loc='best')
        plt.show()



if __name__=='__main__':
    binary_perceptron = BinaryPerceptron(alpha=0.5)
    pbp = PlotRingBP(binary_perceptron, map = True) # remapped
    # pbp = PlotRingBP(binary_perceptron)
    pbp.train()
    pbp.plot()
