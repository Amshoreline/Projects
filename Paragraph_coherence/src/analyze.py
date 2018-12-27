#这只是一个辅助程序，用于分析数据的组成情况
def analyze(text_file):
    with open(text_file, 'r') as reader:
        texts = eval(reader.read())
        max_sent_len = 0        #一个句子中最多单词数
        sent_len = [0] * 175    #统计每个单词数有多少句子对应
        max_sent_num = 0        #一篇文档中最多句子数
        sent_num = [0] * 54     #统计每个句子数由多少文档对应

        for text in texts:
            text = text.split('.')      #按照'.'进行分句
            for sent in text:
                sent = sent.split(' ')  #按照' '进行分词
                if max_sent_len < len(sent):
                    max_sent_len  = len(sent)
                sent_len[len(sent)] = sent_len[len(sent)] + 1
            if max_sent_num < len(text):
                max_sent_num = len(text)
            sent_num[len(text)] = sent_num[len(text)] + 1
        print '一篇文档中最多包含：', max_sent_num, '个句子'
        print '一个句子中最多包含：', max_sent_len, '个单词'
        
        #分析句子中单词数，和文档中的句子数的分布情况
        sum_sent_num = float(sum(sent_num))
        print '文档中句子分布情况如下:'
        for i in range(54):
            print '[', i, sum(sent_num[:i]) / sum_num, ']',

        sum_len_num = float(sum(sent_len))
        print '句子中单词分布情况如下：'
        for i in range(175):
            print '[', i, sum(sent_len[:i]) / sum_num, ']',
if __name__ == '__main__':
    text_files = ['./dataset/train_text', './dataset/test_text', './dataset/valid_text']
    for text_file in text_files:
        analyze(text_file)