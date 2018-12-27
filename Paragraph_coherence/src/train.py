from keras import models
from keras import layers
import numpy as np
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.layers import Dense, Dropout, Input
from keras.layers import Embedding, Concatenate
from keras.models import Model
from keras.models import load_model
from load_glove import load_glove
from read_data import read_data

dim = 50                    #矩阵维数
word2index, matrix = '', '' #word2index字典和矩阵

max_sent_num = 4            #深度学习的句子数目
max_word_num = 5            #每个句子包含最大单词数
index_size = 400001         #word2index中的条目数

number_of_filters = [100]   #隐藏单元个数
kernel_size = [4]           #核数
hidden_layer = 100          #隐藏层
similarity_layer = 20       #相似层的维度

def cnn(x):
    #嵌入层，将单词id映射为词向量
    embedded = Embedding(index_size,
                     dim,
                     weights=[matrix],
                     input_length=max_word_num,
                     trainable=False)(x)
    
    conv_layers = []
    for n_gram, hidden_units in zip(kernel_size, number_of_filters):
        #一维卷积
        conv_layer = Conv1D(filters=hidden_units,
                            kernel_size=n_gram,
                            padding='valid',
                            activation='relu')(embedded)
        #全局最大池化
        conv_layer = GlobalMaxPooling1D()(conv_layer)
        conv_layers.append(conv_layer)

    if len(conv_layers) == 1:
        return conv_layers[0]
    else:
        all_conv_layers_merged = Concatenate()(conv_layers)
        return all_conv_layers_merged
    
def build_model():

    print '加载glove数据'
    global word2index
    global matrix
    glove_file_path = './glove/glove.6B.50d.txt'
    word2index, matrix = load_glove(glove_file_path, 50)
    
    print '建立模型'
    x = []    #x是输入层
    e_x = []  #e_x是第一个隐藏层
    for i in range(max_sent_num):
        print i
        #x[i]对应第i句的输入
        x.append(Input(shape=(max_word_num,)))
        #e_x是嵌入层
        e_x.append(cnn(x[i]))
    
    #句子间的相似度
    s = []   #s是第二个隐藏层
    for i in range(max_sent_num - 1):
        s.append(Dense(units=similarity_layer, 
                        activation='relu')(Concatenate()([e_x[i], e_x[i + 1]])))
    #拼接s层
    join_layer = Concatenate()(s)
    
    #第三个隐藏层
    hidden = Dense(units=hidden_layer, activation='relu')(join_layer)
    hidden = Dropout(0.3)(hidden)

    #输出层
    is_coherent = Dense(units=1, activation='sigmoid')(hidden)
    
    model = Model(inputs=x, outputs=is_coherent)
    return model

if __name__ == '__main__':
    #1.建立模型
    model = build_model()

    #2.读取数据
    train_data_file = './dataset/train_coefs'
    train_label_file = './dataset/train_label'
    valid_data_file = './dataset/valid_coefs'
    valid_label_file = './dataset/valid_label'
    train_data_size = 80000
    valid_data_size = 10000
    y_train, x_train = read_data(train_label_file, train_data_file, train_data_size)
    y_valid, x_valid = read_data(valid_label_file, valid_data_file, valid_data_size)

    #3.编译模型
    model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['acc'])
    print(model.summary())

    #4.训练模型
    model.fit([x_train[i] for i in range(max_sent_num)],
                y_train,
                epochs=4, # 在全数据集上迭代4次
                batch_size=512, # 每个batch的大小为512
                validation_data=([x_valid[i] for i in range(max_sent_num)], y_valid))
    
    #5.保存模型
    model.save('./my_model.h5') 
