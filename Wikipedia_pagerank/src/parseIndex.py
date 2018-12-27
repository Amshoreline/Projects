#读取index文件获得一个排序后的index字符串组
def readIndex(indexFileName):
    #打开index文件并读取
    indexReader = open(indexFileName, 'r')
    indexList = indexReader.read()
    indexReader.close()
    #按照'\n'进行切分
    indexList = indexList.split('\n')
    # 去除indexList每个条目的前缀数字
    indexListSize = len(indexList)
    for i in range(indexListSize):
        tmp = indexList[i].find(':') + 1
        indexList[i] = indexList[i][indexList[i][tmp:].find(':') + 1 + tmp :]
    # 对indexList按照名字进行从小到大排序
    indexList.sort()
    return indexList

#针对indexList生成id和相应的对应字典，并存入本地磁盘
def createDict(indexList, dictPath):
    #由于indexList较大，生成的字典如果直接存入本地磁盘会超出内存容量
    #因此这里分块存储，每个字典各自生成1881个从小到大排序的dictionary blocks
    blockSize = 10000
    blockNum = (indexListSize + blockSize - 1) / blockSize
    firstWords = [] #firstWords表示每个块的第一个词，用于后期索引块
    #两本字典
    name2id = {}
    id2name = {}
    #先处理前blockNum - 1个块
    for i in range(blockNum - 1):
        dictFile_n = open(dictPath + 'name2id_' + str(i) + '.txt', 'w')
        dictFile_i = open(dictPath + 'id2name_' + str(i) + '.txt', 'w')
        
        offset = i * blockSize
        name2id[indexList[offset]] = offset
        id2name[offset] = indexList[offset]
        firstWords.append(indexList[offset])
        for j in range(1, blockSize):
            name2id[indexList[offset + j]] = offset + j
            id2name[offset + j] = indexList[offset + j]
        dictFile_n.write(str(name2id))
        dictFile_i.write(str(id2name))
        
        name2id.clear()
        id2name.clear()
        dictFile_n.close()
        dictFile_i.close()    
    #最后一块特殊处理
    if blockNum >= 1:
        i = blockNum - 1
        dictFile_n = open(dictPath + 'name2id_' + str(i) + '.txt', 'w')
        dictFile_i = open(dictPath + 'id2name_' + str(i) + '.txt', 'w')
        
        offset = i * blockSize
        name2id[indexList[offset]] = offset
        id2name[offset] = indexList[offset]
        firstWords.append(indexList[offset])
        size = min(blockSize, indexListSize - offset)
        for j in range(1, size):
            name2id[indexList[offset + j]] = offset + j
            id2name[offset + j] = indexList[offset + j]
        dictFile_n.write(str(name2id))
        dictFile_i.write(str(id2name))
        
        name2id.clear()
        id2name.clear()
        dictFile_n.close()
        dictFile_i.close()
    #存储和字典有关的信息
    dictInfoFile = open(dictPath + 'dictInfo.txt', 'w')
    dictInfoFile.write(str(blockSize) + '\n' + str(blockNum) + '\n')
    dictInfoFile.write(str(firstWords))
    dictInfoFile.close()


if __name__ == '__main__':
    indexFileName = u'enwiki-20181001-pages-articles-multistream-index.txt'
    indexList = readIndex(indexFileName)

    dictPath = './dict/'
    
