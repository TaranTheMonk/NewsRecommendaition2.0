##Suppose we already have user's previous reading vectors
##Here we'll try to give recommendations from it.
import json
import pandas as pd

class loadFunction():

    def loadSimilarityScore(self):
        with open('sampleSimilarityDict.json', 'r', encoding='utf-8') as f:
            similarities = json.load(f)
        f.close()
        simMatrix = pd.DataFrame(similarities)
        return simMatrix

    def loadReadingHistory(self):
        return

class recommendationFunction():
    def mergeSort(self):
        return

    def findSimilarPeople(self, simMatrix):
        similarDict = dict()
        for deviceId in simMatrix.columns:
            similarDict[deviceId] = list()

        return

    def giveRecommendation(self):
        return


def main():
    return