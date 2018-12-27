import numpy as np
import matplotlib.pyplot as plt
from matplotlib import mlab
from matplotlib import rcParams

#'''第一部分
#绘制一定聚类数的聚类大小分布图
clusterpath = "D:\mydata\\b_output\\result\clusterapi_15.txt"
reader = open(clusterpath, 'r', encoding='utf-8')

fig1 = plt.figure(2)
lefts = ()
heights = ()
tmp = []
numOfClusters = 15  #聚类的个数
num = 0    #应用的个数
for i in range(numOfClusters):
    lefts = lefts + (0.02 * (i + 1), )
    tmp.append(0)
for eachline in reader:
    n = int(eachline.split(':::')[1])
    tmp[n] = tmp[n] + 1
    num = num + 1
print("一共有" + str(num) + "个应用")
maxsize = 0  #最大的聚类大小
minsize = num + 1
for i in range(numOfClusters):
    if maxsize < tmp[i]:
        maxsize = tmp[i]
    if minsize > tmp[i]:
        minsize = tmp[i]
    heights = heights + (tmp[i], )
print("最大的聚类大小是" + str(maxsize) + " 最小的聚类大小是" + str(minsize))

rects = plt.bar(left=lefts, height=heights, width=0.01, align="center", yerr=0.000001)
plt.title('Size of clusters')
first = (0.02, )
second = ('1', )
for i in range(int(numOfClusters / 10)):
    first = first + ((0.2 + 0.2 * i), )
    second = second + (str(10 + 10 * i), )
plt.xticks(first, second)
#plt.xticks((0.02, 0.2, 0.4, 0.6), ('1', '10', '20', '30'))
#plt.xticks((0, 0.6, 1.2, 1.8, 2.4), ('0', '30', '60', '90', '120'))
plt.xlabel("Cluster No.")
plt.ylabel("Cluster Size")
plt.show()
#'''
'''
#第二部分
#绘制不同聚类数（K值）的分布情况，table是kmeansTrain.py生成的数据
table = [
5,355530.2642204044,
6, 338911.561318257,
7, 326295.855104107,
8, 315750.033447334,
9, 306417.93285774963,
10,300382.7417749023,
11,295142.76580372656,
12,290651.42783041287,
13,286237.5672747176,
14,281782.8966219236,
15,278595.431208751,
16,275708.9866239756,
17,271153.89422679384,
18,268043.7300520849,
19,265801.96550583286,
20,263966.3643157927,
21,260853.85376994906,
22,258916.7356172777,
23,257100.48003451235,
24,254341.95428696804,
25,251828.20509362168,
26,249079.82456820074,
27,248258.14141017478,
28,244570.5942376424,
29,243795.4993759517,
30,241440.35674408093,
31,240178.5414192006,
32,240338.70472726654,
33,235445.1551266757,
34,236097.580509174,
35,234120.33866557857,
36,232216.6449581446,
37,232093.20332124433,
38,230128.40694557037,
39,228718.682337655,
40,227844.89417410578,
41,226717.93888648608,
42,224704.65634675467,
43,223885.76743447673,
44,222708.91467394316,
45,221578.96611008456,
46,219067.65531777107,
47,220140.34595637937,
48,218762.63205367012,
49,216808.1516133617,
50,217049.80524628877,
51,215195.04122048663,
52,214924.26675121268,
53,214792.2865824341,
54,212885.8714874691,
55,211163.48300644755,
56,210867.445772825,
57,209084.712191232,
58,208903.98446975392,
59,208524.173809834]

y = []
names = []

for i in range(0, 54, 1):
    y.append(table[2 * i + 1] - table[2 * i + 3])
    if i % 5 == 0:
        names.append(str(i + 5))
    else:
        names.append('')
x = range(54)
###
for i in range(0, 55, 1):
    y.append(table[2 * i + 1])
    if i % 5 == 0:
        names.append(str(i + 5))
    else:
        names.append('')
x = range(55)

plt.plot(x, y, linewidth=2, marker='o')
plt.xticks(x, names)
plt.xlabel('number of clusters')
plt.ylabel('mean distance')
plt.title('variation tendency ')
plt.legend()
plt.show()
'''