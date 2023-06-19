import seaborn as sb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

time1 = pd.read_csv("testTime.csv")
time = np.log(time1.iloc[:, 1:].values)
evalTime = pd.read_csv("timeForEval.csv")

evalTi = np.log(evalTime.iloc[:, 1:].values)


sb.heatmap(time,xticklabels=time1.columns[1:], yticklabels=time1.iloc[:, 0])

plt.figure(2)
sb.heatmap(evalTi,xticklabels=evalTime.columns[1:], yticklabels=evalTime.iloc[:, 0])