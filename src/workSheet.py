##try other way to compute cos-similarity
import json
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import math

with open('sample-relationshipTable.json', 'r', encoding='utf-8') as f:
    relationship = json.load(f)
f.close()

sumSim = []
for item in similarities:
    if round(item.sum(), 3) > 1:
        sumSim.append(item.sum())
plt.hist(sumSim, 100)

recordList = []
for item in similarities:
    for record in item:
        if round(record, 3) != 0 and round(record, 3) != 1:
            recordList.append(record)
plt.hist(recordList, 100)