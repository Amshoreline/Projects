from itertools import izip

#定义一个IdList的class，用于检索某个出链指向的页面是否属于170万样本页面
class IdList:
    def __init__(self):
        self.ilist = []
        self.listSize = 0
    def addId(self, i):
        self.ilist.append(i)
        self.listSize = self.listSize + 1
    def sortList(self):
        self.ilist.sort()
    #findId采用二分查找优化查找速度
    def findId(self, i):
        left = 0
        right = self.listSize
        while left < right:
            middle = (left + right) / 2
            if i < self.ilist[middle]:
                right = middle
                continue
            if i > self.ilist[middle]:
                left = middle + 1
                continue
            return True
        return False

#定义图中节点所对应的class
class Node:
    def __init__(self, i, out):
        self.nodeId = i
        self.outList = out

#从磁盘中导入之前解析出的“图”
def loadGraph(idFile, nodeFile):
    if idFile != '':
        idReader = open(idFile, 'r')
        idList = IdList()
        idList.listSize = int(idReader.readline())
        idList.ilist = eval(idReader.read())
        idReader.close()
    nodeReader = open(nodeFile, 'r')
    nodes = []
    while True:
        string = nodeReader.readline()
        if string == '':
            break
        string = string.split(':::')
        node = Node(int(string[0]), eval(string[1]))
        nodes.append(node)
    nodeReader.close()
    
    return idList, nodes

#将图中的出边转换为入边，并将结果存入本地磁盘
def trainsform(idList, nodes):
    linkList = []        #linkList的元素是整数的list
    outSizeList = []     #每个页面出链数统计
    nodeNum = len(nodes) #页面个数
    dictionary = {}      #从页面ID到数组下标的字典
    invDict = {}         #从数组下表到页面ID的字典

    #初始化
    for i in range(nodeNum):
        outSizeList.append(0)
        linkList.append([])
        dictionary[idList.ilist[i]] = i
    #将出链转为入链
    #最终linkList中的每个list存储的整数都代表页面ID对应的数组下标
    for node in nodes:
        firstNode = dictionary[node.nodeId]
        outSizeList[firstNode] = len(node.outList)
        for outNodeId in node.outList:
            secondNode = dictionary[outNodeId]
            linkList[secondNode].append(firstNode)

    #获得反转字典
    invDict = dict(izip(dictionary.itervalues(), dictionary.iterkeys()))
    # 所以两本字典的映射关系如下
    # dictionary: nodeId => storageId
    # invDict:    storageId => nodeId

    #将结果存入本地磁盘
    dictFile = './final/dict.txt'
    invDictFile = './final/invDict.txt'
    linkListFile = './final/cList.txt'
    outSizeListFile = './final/outSizeList.txt'
    writerD = open(dictFile, 'w')
    writerI = open(invDictFile, 'w')
    writerL = open(linkListFile, 'w')
    writerO = open(outSizeListFile, 'w')
    writerD.write(str(dictionary))
    writerI.write(str(invDict))
    writerO.write(str(outSizeList))
    for i in range(nodeNum):
        writerL.write(str(len(linkList[i])))
        writerL.write(str(linkList[i]) + '\n')
    writerD.close()
    writerI.close()
    writerL.close()
    writerO.close()
    
if __name__ == '__main__':
    idFile = './graph/idList.txt'
    nodeFile = './graph/nodeList.txt'
    idList, nodes = loadGraph(idFile, nodeFile)
    #将nodes按照nodeId从小到大排序
    nodes.sort(key=lambda node:node.nodeId)
    transform(idList, nodes)
    
