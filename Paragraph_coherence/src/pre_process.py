#读取作业给定的原文件，分离出文本和标签到不同文件夹中
def PreProcess(src_file, label_file, text_file):
    print src_file, label_file, text_file
    with open(src_file, 'r') as reader:
        lines = reader.readlines()
        labels = []
        texts = []
        for line in lines:
            tmp_dict = eval(line)
            labels.append(int(tmp_dict['label']))
            texts.append(tmp_dict['text'])
        with open(label_file, 'w') as writer:
            writer.write(str(labels))
        with open(text_file, 'w') as writer:
            writer.write(str(texts))        
if __name__ == '__main__':
    src_files = ['./data/train_data', './data/test_data', './data/valid_data']
    label_files = ['./dataset/train_label', './dataset/test_label', './dataset/valid_label']
    text_files = ['./dataset/train_text', './dataset/test_text', './dataset/valid_text']
    for i, src_file in enumerate(src_files):
        PreProcess(src_file, label_files[i], text_files[i])