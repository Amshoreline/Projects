第一步：基于API调用特征的Kmeans聚类
代码文件及运行顺序介绍：
核心代码：
randomSet.py: 将数据集随机分配为训练集或测试集
   ||
   \/
apiExtracter.cpp: 分析从每个app提取出的API描述文件，得出API被调用情况和应用调用API种类情况
   ||
   \/
apiAnalyzer.cpp: 统计各个API被调用的情况，排除被调用次数过少的API
   ||
   \/
apiFeatCreator.cpp: 生成每个应用的API调用特征向量
   ||
   \/
kmeansTrain.py: 根据应用的API调用特征向量调用Kmeans进行聚类
   ||
   \/
kmeansPredict.py: 为测试集的应用预测其所属的聚类

辅助代码：
whitelistCreator.cpp: 分析训练集和测试集，提取白名单
drawTable: 绘制kmeans聚类相关的图像
