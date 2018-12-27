import os
import random
import time

time_start = time.time()
# 生成训练集和测试集
fineCnt = 3400      #两类应用的总数
malCnt = 989
fineTest = (int)(fineCnt / 10)  #fineTestSet的大小
malTest = (int)(malCnt / 10)    #malTestSet的大小
fineApiPath = "D:\mydata\\apilist\\apilist_for_fineware"
malApiPath = "D:\mydata\\apilist\\apilist_for_malware"

#这里先只提取前10%的程序作为训练集，后续再引入随机
whitePath = "D:\mydata\\apilist\white.txt"
testListPath = "D:\mydata\\apilist\\testList.txt"
trainListPath = "D:\mydata\\apilist\\trainList.txt"

whiteList = open(whitePath, 'w', encoding='utf-8')
testList = open(testListPath, 'w', encoding='utf-8')
trainList = open(trainListPath, 'w', encoding='utf-8')

#生成随机数
testSet = set()
while len(testSet) < fineTest:
    testSet.add(random.randint(0, fineCnt))

#读取目录
pathDir = os.listdir(fineApiPath)
cnt = 0
for smallItem in pathDir:
    if smallItem.endswith('.apk.txt'):
        if (cnt in testSet):
            testList.write('1:::' + smallItem[0:-8] + '\n')
        else:
            whiteList.write(smallItem[0:-8] + '\n')
            trainList.write('1:::' + smallItem[0:-8] + '\n')
    cnt = cnt + 1

#生成随机数
testSet.clear()
while len(testSet) < malTest:
    testSet.add(random.randint(0, malCnt))

#读取目录
pathDir = os.listdir(malApiPath)
cnt = 0
for smallItem in pathDir:
    if smallItem.endswith('.apk.txt'):
        if (cnt in testSet):
            testList.write('0:::' + smallItem[0:-8] + '\n')
        else:
            whiteList.write(smallItem[0:-8] + '\n')
            trainList.write('0:::' + smallItem[0:-8] + '\n')
    cnt = cnt + 1

time_end = time.time()
print("用时" + str(time_end - time_start) + "秒")