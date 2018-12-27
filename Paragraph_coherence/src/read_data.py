import numpy as np

def read_data(label_file, data_file, data_size):
    sent_num = 4
    word_num = 5
    data = np.zeros([sent_num, data_size, word_num], dtype='int')
    labels = []
    with open(data_file, 'r') as reader:
        lines = reader.readlines()
        for i, line in enumerate(lines):
            line = eval(line)[0:sent_num]
            len1 = min(sent_num, len(line))
            for j in range(len1):
                len2 = min(word_num, len(line[j]))
                for k in range(len2):
                    data[j][i][k] = line[j][k]
    with open(label_file, 'r') as reader:
        labels = eval(reader.read())
        print len(labels) == data_size
    labels = np.asarray(labels).astype('float32')
    return labels, data
