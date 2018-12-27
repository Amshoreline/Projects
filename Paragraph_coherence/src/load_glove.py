import numpy as np

#读取glove中已经训练好的数据，为其中所有的单词生成一个矩阵
#矩阵的行索引是单词的index，每一行代表一个单词的向量表示

#输入是glove文档的路径，dim是生成矩阵的列向量数
#输出是word2index的字典和上述矩阵matrix
def load_glove(file_name, dim):
    #首先建立word2index的字典，和一个word2coefs的字典，之后会用word2coefs建立目标矩阵
    word2coefs = {}
    word2index = {}
    with open(file_name, 'r') as f:
        for idx, line in enumerate(f):
            try:
                data = [x.strip().lower() for x in line.split()]
                word = data[0]
                coefs = np.asarray(data[1:dim + 1], dtype='float32')
                word2coefs[word] = coefs
                if word not in word2index:
                    word2index[word] = len(word2index)
            except Exception as e:
                print('Error:', e)
                continue
    word2index[''] = len(word2index)  #将空字符串纳入考虑

    #其次是构建目标矩阵
    word_num = len(word2coefs) + 1
    matrix = np.zeros((word_num, dim))
    for word, idx in word2index.items():
        vector = word2coefs.get(word)
        if vector is not None and vector.shape[0] == dim:
            matrix[idx] = np.asarray(vector)
    return word2index, np.asarray(matrix)