##try other way to compute cos-similarity
import json
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

with open('newsPoolDict.json', 'r', encoding ='utf-8') as f:
    pool = json.load(f)
f.close()

sim = pd.DataFrame(pool)
sim = np.array(sim.values.tolist())
sim = sim.reshape(1,1000*1000)[0]
plotSim = list()
for i in sim:
    if i != 1:
        plotSim.append(i)

a = plt.hist(plotSim, 100, color='g')
plt.xlabel('Similarity')
plt.ylabel('Count')
plt.title('Histogram of Similarity')
plt.grid(True)