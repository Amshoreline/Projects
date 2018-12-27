import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.externals import joblib
import time

path = "D:\mydata\\b_output"
modelFile = path + "\\result\model.pkl"
x = []
name = []

#'''clustering

time_start = time.time()
clusterFile = path + "\\result\\clusterapi.txt"
clusterWriter = open(clusterFile, 'w', encoding='utf-8')
info = open(path + "\\result\\information.txt", 'w', encoding='utf-8') #相关数据

f = open(path + "\\train\\trainApi.txt")
num = open(path + "\\train\\apiVector.txt").read()
num = int(num)

print("start clustering")

cnt = 0
for v in f:
    name.append(v.split(',')[0])
    y = []
    for i in range(num):
        y.append(float(v.split(',')[i + 1]))
    x.append(y)
    cnt = cnt + 1
print("应用数是" + str(cnt))
#转换成numpy array
x = np.array(x)
#聚类的数量

#for i in range(5, 60, 1):
#    cls = KMeans(i).fit(x)
#    print(str(i) + "," + str(cls.inertia_))

n_clusters = 40
#把数据和对应的分类放入聚类函数中进行聚类
cls = KMeans(n_clusters).fit(x)
#x中每项所属分类的一个列表
print("test")

i = 0
for eachline in name:
    clusterWriter.write(eachline + ":::")
    clusterWriter.write(str(cls.labels_[i]) + '\n')
    #print(eachline, end=' ')
    #print(str(cls.labels_[i]))
    i = i + 1
info.write(str(i))
#保存模型
joblib.dump(cls, modelFile)
time_end = time.time()
print("done")
print('totally cost', time_end - time_start, 'seconds')