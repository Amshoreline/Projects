#include <iostream>
#include <cstring>
#include <vector>
#include <cmath>
#include <string>
#include <fstream>
using namespace std;

const int graphSize = 1726903;      //之前从xml中读取出了1726903个网页相关数据 
float list_1[graphSize], list_2[graphSize];  //存储所有网页的weight(本代码用"weight"指代"pagerank")的值 
float *weightList, *tmpWeightList;  //指向weight数组的指针 
int outSizeList[graphSize];			//outSizeList中每个元素代表相应网页的出边数 
vector<int>* linkList[graphSize];   //graphSize大小的vector数组，每个vector标示了连接到此网页的网页们

//从磁盘中导入“图” 
void loadGraph()
{
	// 1.读取outSizeList，即每个网页的出边数 
	cout << "load the outSizeList" << endl;
	char c;
	string file = "D:\\Jupyterspace\\pagerank\\final\\outSizeList.txt";
	ifstream infile;
	 
	infile.open(file.data());
	if (!infile.is_open())
	{
		cout << "Failed to open the file: " << file << endl;
		return;
	}
    
	infile >> c;
	for (int i = 0; i < graphSize; ++i)
	{
		infile >> outSizeList[i] >> c;
	}
	infile.close();
    
	// 2.读取linkList，即每个网页被连接的情况 
	cout << "load the linkList" << endl;
	file = "D:\\Jupyterspace\\pagerank\\final\\cList.txt";
	infile.open(file.data());
	if (!infile.is_open())
	{
		cout << "Failed to open the file: " << file << endl;
		return;
	}
	int vSize;
	for (int i = 0; i < graphSize; ++i)
	{
		infile >> vSize;
		linkList[i] = new vector<int>(vSize);
		infile >> c;
		for (int j = 0; j < vSize; ++j)
		{
			infile >> (*linkList[i])[j] >> c;
		}
		if (vSize == 0)
			infile >> c;
	}
	infile.close();
}

//计算pageRank的函数 
void pageRank()
{
	float dampingFactor = 0.85;  // α
	int maxIterations = 100;     // 最大迭代次数
	float minDelta = 0.0001;      // 确定迭代是否结束的参数
    
	//先将图中没有出边的节点改为对所有节点都有出边 （本代码中“节点”就是“页面”） 
	//这里用zeroList存储所有没有出边的节点，之后在迭代中特殊处理它们 
	vector<int> zeroList;
	for (int i = 0; i < graphSize; ++i)
	{
    		weightList[i] = 1.0 / graphSize;   // Page 的权值，给每个节点赋予初始的weight为1 / N
		if (outSizeList[i] == 0)           //如果没有出边，就把节点加入zeroList中 
			zeroList.insert(zeroList.end(), i);
	}
        
	float dampingValue = (1.0 - dampingFactor) / graphSize;  // 公式中的(1-α)/N部分
	float change, left;  //change表示一次迭代中的改变量，left表示公式等号右边中的不是 (1-α)/N的那部分
	vector<int>::iterator k;
    
	for (int i = 0; i < maxIterations; ++i)
	{
		cout << "Iteration: " << i << endl;
		change = 0;
    	
		//遍历图中的每个节点 
		for (int j = 0; j < graphSize; ++j)
		{
    			left = 0;
    		
    			//对每个节点，left表示：指向该节点的那些节点的 weight值/出边数 之和 
			for (k = linkList[j]->begin(); k < linkList[j]->end(); ++k)
				left += weightList[*k] / outSizeList[*k];
    			
			//  这里为了节省内存，假定没有出边的节点变成指向图中所有节点(包括自己)后，用zeroList存储
			//这些没有出边的节点，然后特别处理这些特殊节点，因此left要加上这些节点的 权值/图中节点个数 
			for (k = zeroList.begin(); k < zeroList.end(); ++k)
				left += weightList[*k] / graphSize;
			
			//tmpWeightList指向的数组存储的是：该图中每个节点新一轮迭代得到的新的权值 
			tmpWeightList[j] = dampingFactor * left + dampingValue;
			
			//累加迭代中每个节点权值的改变量 
			change += abs(tmpWeightList[j] - weightList[j]);
		}
		
		//这里表示一轮迭代结束后，更新图中节点权值的过程：
		//为了加快计算速度，这里直接让weightList指向tmpWeightList指向的数组，
		//tmpWeightList指向weightList之前指向的数组
		//相当于把tmpWeightList的值“赋”给了weightList 
		float *tmp = weightList;
		weightList = tmpWeightList;
		tmpWeightList = tmp;
		
		cout << "Change = " << change << endl;
		//如果改变量小于minDelta，终止迭代 
		if (change < minDelta)
			break;
	}
}

//将最终计算结果存入本地磁盘 
void saveWeightList()
{
	ofstream outfile;
	outfile.open("D:\\Jupyterspace\\pagerank\\final\\weight.txt");
	if (!outfile.is_open())
	{
		cout << "Failed to open the file: " << 
		     "D:\\Jupyterspace\\pagerank\\final\\weight.txt" << endl;
		return;
	}
	outfile << '[';
	for (int i = 0; i < graphSize; ++i)
		outfile << weightList[i] << ',';
	outfile << ']';
}

int main()
{
	loadGraph();
	
	//weightList指向list_1, tmpWeightList指向list_2 
	weightList = list_1;
	tmpWeightList = list_2;
	
	cout << "start pageRank()" << endl;
	pageRank();
	
	cout << "save the weightList" << endl;
	saveWeightList();
	
	return 0;
} 