import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import time

time_start = time.time();
testFile = path + "\\test\\testApi.txt"
testReader = open(testFile, 'r', encoding='utf-8')
resultFile = path + "\\test\\testCluster.txt"
resultWriter = open(resultFile, 'w', encoding='utf-8')
num = open(path + "\\test\\apiVector.txt").read()
num = int(num)
f = open(testFile)
cnt = 0
for v in f:
    name.append(v.split(',')[0])
    y = []
    for i in range(num):
        y.append(float(v.split(',')[i + 1]))
    x.append(y)
    cnt = cnt + 1
print("应用数是" + (str)(cnt))

print("start predicting")
x = np.array(x)
cls = joblib.load(modelFile)

i = 0
p = cls.predict(x)
for eachline in name:
    resultWriter.write(eachline + ":::")
    resultWriter.write(str(p[i]) + '\n')
    i = i + 1
print("done")
time_end = time.time();
print('totally cost', time_end - time_start, 'seconds')