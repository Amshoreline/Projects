import load_glove

#删除句号以外的标点符号
def remove_non_letter(text):
    text = text.lower()
    return ''.join([i if (ord(i) < 123 and ord(i) > 96) or ord(i) == 46 else ' ' for i in text])

def word_to_coefs(text_file, coefs_file, word2index):
    print text_file, coefs_file

    #根据之前analyze.py处理结果显示，90%文档包含至多16个句子，90%的句子包含至多40个单词
    #因此这里对每篇文档，至多只取到16个句子；对每个句子，至多只取到40个单词
    max_sent_num = 16
    max_word_num = 40
    
    cnt = 0
    error_cnt = 0
    
    with open(text_file, 'r') as reader:
        texts = eval(reader.read())
        with open(coefs_file, 'w') as writer:
            for text in texts:
                vectors = []
                #删除句号以外的标点符号
                text = remove_non_letter(text)
                
                sents = text.split('.')         #分句
                sent_num = len(sents)
                sent_parse_num = min(max_sent_num, sent_num)
                
                for i in range(sent_parse_num):
                    vector = []
                    
                    sent = sents[i]
                    words = sent.split(' ')     #分词
                    word_num = len(words)
                    word_parse_num = min(max_word_num, word_num)
                    for j in range(word_parse_num):
                        if words[j] in word2index:
                            vector.append(word2index[words[j]])
                        else:
                            error_cnt = error_cnt + 1
                            vector.append(word2index[''])
                    vectors.append(vector)
                writer.write(str(vectors) + '\n')
#end of word_to_coefs
                
if __name__ == '__main__':
    #加载glove中已经训练好的数据
    glove_file_path = './glove/glove.6B.50d.txt'
    word2index, matrix = load_glove(glove_file_path, 50)

    #以此处理所有文本，生成对应的coefs文件，coefs文件每行代表一个文档，文档由一个二维list表示
    #元素是代表句子的list，代表句子list的元素是其中单词的index值
    text_files = ['./dataset/train_text', './dataset/test_text', './dataset/valid_text']
    coefs_files = ['./dataset/train_coefs', './dataset/test_coefs', \
                   './dataset/valid_coefs']
    for i, text_file in enumerate(text_files):
        word_to_coefs(text_file, coefs_files[i], word2index)