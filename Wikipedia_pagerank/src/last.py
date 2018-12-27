
#定义每个页面相关的class
class Page:
    def __init__(self, n, w):
        self.name = n
        self.weight = w
#所有页面的class，用于页面按照weight（也就是pageRank值）进行从大到小排序
class PageRanking:
    def __init__(self, pList):
        self.pageList = pList
        self.listSize = len(pList)
    def sort(self):
        self.pageList.sort(key=lambda x:x.weight, reverse=True)

#读取磁盘中<id, name>的字典到内存中
def loadIdToName():
    dictPath = './dict/'
    dictInfoFile = open(dictPath + 'dictInfo.txt', 'r')
    blockSize = int(dictInfoFile.readline())
    blockNum = int(dictInfoFile.readline())
    dictInfoFile.close()
    
    dictionary = {}
    for i in range(blockNum):
        dictFile = open(dictPath + 'id2name_' + str(i) + '.txt', 'r')
        tmpDict = eval(dictFile.read())
        dictionary.update(tmpDict)
    return dictionary

#读取磁盘中<storageId, pageId>的字典到内存中
def loadInvDict():
    fileName = './final/invDict.txt'
    reader = open(fileName, 'r')
    invDict = eval(reader.read())
    reader.close()
    return invDict

#读取磁盘中每个页面的pageRank值数组到内存中(这里weight代表pageRnak值)
def loadWeightList():
    fileName = './final/weight.txt'
    reader = open(fileName, 'r')
    weightList = eval(reader.read())
    reader.close()
    return weightList

if __name__ == '__main__':
    id2name = loadIdToName()
    invDict = loadInvDict()
    weightList = loadWeightList()
    
    graphSize = len(weightList)
    pList = []
    #将最终结果转换成Page类实例，并组装到PageRanking的实例中
    for i in range(size):
        name = id2nameDict[invDict[i]]   #获取页面的真正名字
        page = Page(name, weightList[i])
        pList.append(page)
    pageRanking = PageRanking(pList)

    #对结果进行排序
    pageRanking.sort()
    #把结果写入磁盘中
    writer = open('./final/result.txt', 'w')
    for i in range(1000000): #取前100万存入磁盘
        writer.write(str(pageRanking.pageList[i].name) + ' \t ' + str(pageRanking.pageList[i].weight) + '\n')
    writer.close()
