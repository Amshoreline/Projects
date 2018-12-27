import re

#字典索引函数，通过读取存入本地的字典进行从name索引到id和从id索引到name
def nametoid(n, dictPath):
    dictInfoFile = open(dictPath + 'dictInfo.txt', 'r')
    blockSize = int(dictInfoFile.readline())
    blockNum = int(dictInfoFile.readline())
    firstWords = eval(dictInfoFile.readline())
    dictInfoFile.close()
    
    dictIndex = 0
    for dictIndex in range(blockNum):
        if n < firstWords[dictIndex]:
            dictIndex = dictIndex - 1
            break
    
    dictFile = open(dictPath + 'name2id_' + str(dictIndex) + '.txt', 'r')
    dictionary = eval(dictFile.read())
    try:
        i = int(dictionary[n])
    except KeyError as e:
        i = -1
    dictionary.clear()
    dictFile.close()
    return i

def idtoname(i, dictPath):
    dictInfoFile = open(dictPath + 'dictInfo.txt', 'r')
    blockSize = int(dictInfoFile.readline())
    blockNum = int(dictInfoFile.readline())
    dictInfoFile.close()

    dictIndex = i / blockSize
    
    dictFile = open(dictPath + 'id2name_' + str(dictIndex) + '.txt', 'r')
    dictionary = eval(dictFile.read())
    try:
        n = dictionary[i]
    except KeyError as e:
        n = '_'
    dictionary.clear()
    dictFile.close()
    return n

#读取磁盘中<name, id>的字典到内存中
def loadDict(dictPath):
    dictInfoFile = open(dictPath + 'dictInfo.txt', 'r')
    blockSize = int(dictInfoFile.readline())
    blockNum = int(dictInfoFile.readline())
    dictInfoFile.close()
    
    dictionary = {}
    for i in range(blockNum):
        dictFile = open(dictPath + 'name2id_' + str(i) + '.txt', 'r')
        tmpDict = eval(dictFile.read())
        dictionary.update(tmpDict)
    return dictionary

#解析一个Page页的XML信息
def parsePage(xml, blockSize, dictionary):
    #正则表达式匹配解析页面名
    name = re.findall('<title>(.*?)</title>', xml)[0].lower()
    #查找字典找到页面名对应的ID
    if dictionary == {}:
        pageId = nametoid(name)
    else:
        try:
            pageId = dictionary[name]
        except KeyError as e:
            pageId = -1
    if pageId == -1:
        print 'Failed to get the page id'
        return
    #通过正则表达式匹配找到该页面的出链指向的其他页面的ID
    blockNum = pageId / blockSize
    referLists = re.findall('\[\[(.*?)\]\]', xml)
    referLists = referLists + re.findall('redirect title="(.*?)"', xml)
    outList = []
    for items in referLists:
        #对于有用'|'分开的多个出链页面字符串，直接按照'|'进行瓜分
        itemList = items.split('|')
        for item in itemList:
            if dictionary == {}:
                tmpId = nametoid(item)
            else:
                try:
                    tmpId = dictionary[item]
                except KeyError as e:
                    tmpId = -1
            if tmpId != -1:
                outList.append(tmpId)
    #将解析结果写入本地磁盘
    #和存储字典一样，分块存入磁盘
    writeFile = './xml/xml_' + str(blockNum) + '.txt'
    writer = open(writeFile, 'a')
    writer.write(str(pageId) + ':::')
    writer.write(str(outList))
    writer.write('\n')
    writer.close()

#读取XML文件并进行分析
def readXml(xmlFileName, dictPath):
    xmlReader = open(xmlFileName, 'r')
    xmlStr = ''        #用于存储一个页面的XML字符串
    blockSize = 10000  #分块存储分析结果中块的大小
    pageNum = 0        #计数读入的page数
    
    #导入name到id映射的字典
    dictionary = loadDict(dictPath)
    #循环按行读取维基百科给的XML文件
    while True:
        xmlStr = xmlReader.readline()
        if xmlStr == '':
            break
        #如果读到<page>说明读到了一个页，进入另一个循环读取整个页的数据并解析
        if xmlStr.find('<page>') != -1:
            pageNum = pageNum + 1
            #如果已经读了170万页面就退出循环
            if pageNum > 1700000:
                break
            #开始读取一个页的数据，直到读入</page>
            pageStr = xmlStr
            while True:
                xmlStr = xmlReader.readline()
                if xmlStr == '':
                    break
                pageStr = pageStr + xmlStr
                if xmlStr.find('</page>') != -1:
                    break
            parsePage(pageStr, blockSize, dictionary)
    xmlReader.close()    

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
        
#整理解析出的“图”
def vaidLinks():
    xmlDir = './xml/'
    #由于之前图是分块存储的，且图中节点组成的块和字典中的块是一一对应的
    dictInfoFile = open('./dict/dictInfo.txt', 'r')
    blockSize = int(dictInfoFile.readline())
    blockNum = int(dictInfoFile.readline())
    dictInfoFile.close()
    nodeList = []
    idList = IdList()

    #分块整理
    for i in range(blockNum):
        fileName = xmlDir + 'xml_' + str(i) + '.txt'
        if os.path.exists(fileName):
            xmlReader = open(fileName, 'r')
            while True:
                nodeStr = xmlReader.readline()
                if nodeStr == '':
                    break
                nodeStr = nodeStr.split(':::')
                nodeId = int(nodeStr[0])
                #去除出链重复项
                outList = list(set(eval(nodeStr[1])))
                nodeList.append(Node(nodeId, outList))
                idList.addId(nodeId)
            xmlReader.close()
    return idList, nodeList

# 删除无用的link，即不指向这170万样本页面的出链
def slimGraph(idList, nodeList):
    nodeNum = len(nodeList)
    i = 0
    while i < nodeNum:
        #出链个数
        outNum = len(nodeList[i].outList)
        j = 0
        while j < outNum:
            if idList.findId(nodeList[i].outList[j]):
                j = j + 1
            else:
                nodeList[i].outList.pop(j)
                outNum = outNum - 1
        i = i + 1

#将整理后的图存入本地磁盘
def saveGraph(idList, nodeList, idFile, nodeFile):
    idWriter = open(idFile, 'w')
    nodeWriter = open(nodeFile, 'w')
    idWriter.write(str(idList.listSize) + '\n')
    idWriter.write(str(idList.ilist))
    for node in nodeList:
        nodeWriter.write(str(node.nodeId) + ':::')
        nodeWriter.write(str(node.outList) + '\n')
    idWriter.close()
    nodeWriter.close()

if __name__ == '__main__':
    dictPath = './dict/'
    xmlFileName =  u'enwiki-20181001-pages-articles-multistream.xml'
    readXml(xmlFileName, dictPath)

    idList, nodeList = vaidLinks()
    slimGraph(idList, nodeList)
    
    idFile = './graph/idList.txt'
    nodeFile = './graph/nodeList.txt'
    saveGraph(idList, nodeList, idFile, nodeFile)
    
