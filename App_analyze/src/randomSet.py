import os
import random
import time

time_start = time.time()
# ����ѵ�����Ͳ��Լ�
fineCnt = 3400      #����Ӧ�õ�����
malCnt = 989
fineTest = (int)(fineCnt / 10)  #fineTestSet�Ĵ�С
malTest = (int)(malCnt / 10)    #malTestSet�Ĵ�С
fineApiPath = "D:\mydata\\apilist\\apilist_for_fineware"
malApiPath = "D:\mydata\\apilist\\apilist_for_malware"

#������ֻ��ȡǰ10%�ĳ�����Ϊѵ�������������������
whitePath = "D:\mydata\\apilist\white.txt"
testListPath = "D:\mydata\\apilist\\testList.txt"
trainListPath = "D:\mydata\\apilist\\trainList.txt"

whiteList = open(whitePath, 'w', encoding='utf-8')
testList = open(testListPath, 'w', encoding='utf-8')
trainList = open(trainListPath, 'w', encoding='utf-8')

#���������
testSet = set()
while len(testSet) < fineTest:
    testSet.add(random.randint(0, fineCnt))

#��ȡĿ¼
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

#���������
testSet.clear()
while len(testSet) < malTest:
    testSet.add(random.randint(0, malCnt))

#��ȡĿ¼
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
print("��ʱ" + str(time_end - time_start) + "��")