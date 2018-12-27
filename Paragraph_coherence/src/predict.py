from keras.models import load_model
import numpy as np
from read_data import read_data


if __name__ == '__main__':
    max_sent_num = 4
    #1.加载模型
    model = load_model('./my_model.h5')
    
    #2.加载验证和测试数据
    test_data_file = './dataset/test_coefs'
    test_label_file = './dataset/test_label'
    valid_data_file = './dataset/valid_coefs'
    valid_label_file = './dataset/valid_label'
    test_data_size = 10000
    valid_data_size = 10000
    test_labels, test_data = read_data(test_label_file, test_data_file, test_data_size)
    valid_labels, valid_data = read_data(valid_label_file, valid_data_file, valid_data_size)

    #3.预测验证数据
    predict = model.predict([valid_data[i] for i in range(max_sent_num)])
    #预测结果是0~1之间的浮点数，假定预测结果>=0.5表示1，<0.5表示0
    #那么加上valid_labels后，预测正确当且仅当结果在[0, 0.5)和[1.5, 2]中
    for i in range(valid_data_size):
        t = predict[i] + valid_labels[i]
        if t < 0.5 or t >= 1.5:
            predict[i] = 1
        else:
            predict[i] = 0
    

    print sum(predict) / float(len(predict)) #打印预测正确率
    
    #4.预测测试数据
    predict = model.predict([test_data[i] for i in range(max_sent_num)])
    with open('./predict', 'w') as writer:
        for i in range(test_data_size):
            if predict[i] >= 0.5:
                writer.write('1' + '\n')
            else：
                writer.write('0' + '\n')
    
    
