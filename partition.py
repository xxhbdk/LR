import numpy
import pandas
from matplotlib import pyplot as plt

numpy.random.seed(0)


class DataExtract(object):
    
    def __init__(self, filename):
        self.__filename = filename
        self.__oriSheet = self.__get_oriSheet()
        self.__traSheet = self.__get_traSheet()
        
        
    def partition(self, partitionFrac):
        testSet = self.__traSheet.sample(frac=partitionFrac)
        trainingSet = self.__build_trainingSet(testSet, self.__traSheet)
        trainingSet.reset_index(drop=True, inplace=True), testSet.reset_index(drop=True, inplace=True)
        return trainingSet, testSet
        
        
    def __build_trainingSet(self, testSet, sheet):
        oriIndex = sheet.index.isin(testSet.index)
        trainingSet = sheet.loc[~oriIndex]
        return trainingSet
        
        
    def __get_traSheet(self):
        traSheet = self.__oriSheet.copy()
        self.__update_traSheet(traSheet)
        return traSheet
        
        
    def __update_traSheet(self, traSheet):
        traSheet["Class"] = traSheet["Class"].apply(lambda item: 1 if item == 1 else 0)
        
        
    def __get_oriSheet(self):
        oriSheet = pandas.read_csv(self.__filename)
        return oriSheet
        
        
        
class ColorMesh(object):

    def show_data(self, trainingSet, testSet):
        trainingSet0, trainingSet1 = self.__divide_data(trainingSet)
        testSet0, testSet1 = self.__divide_data(testSet)
        
        fig = plt.figure(figsize=(10, 4))
        ax1 = plt.subplot(1, 2, 1)
        ax2 = plt.subplot(1, 2, 2)
        
        ax1.scatter(trainingSet1["At1"].values, trainingSet1["At2"].values, s=20, c="red", edgecolor="k", label="positive")
        ax1.scatter(trainingSet0["At1"].values, trainingSet0["At2"].values, s=20, c="green", edgecolor="k", label="negative")
        ax1.set(xlabel="$At1$", ylabel="$At2$", xlim=[-3.2, 3], ylim=[-2.5, 3.3], title="Distribution on training set")
        ax1.legend()
        
        ax2.scatter(testSet1["At1"].values, testSet1["At2"].values, s=20, c="red", edgecolor="k", label="positive")
        ax2.scatter(testSet0["At1"].values, testSet0["At2"].values, s=20, c="green", edgecolor="k", label="negative")
        ax2.set(xlabel="$At1$", ylabel="$At2$", xlim=[-3.2, 3], ylim=[-2.5, 3.3], title="Distribution on test set")
        ax2.legend()
        
        fig.tight_layout()
        plt.show()
        fig.savefig("show_data.png", dpi=100)
        
        
    def __divide_data(self, sheet):
        sheet0 = sheet.loc[sheet["Class"] == 0]
        sheet1 = sheet.loc[sheet["Class"] == 1]
        return sheet0, sheet1
        
    
    def show_colorMesh(self):
        pass
        
        
        

if __name__ == "__main__":
    obj = DataExtract("banana.dat")
    trainingSet, testSet = obj.partition(0.2)
    
    obj = ColorMesh()
    obj.show_data(trainingSet, testSet)