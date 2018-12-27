#include <iostream>
#include <cstring>
#include <vector>
#include <cmath>
#include <string>
#include <fstream>
using namespace std;

const int graphSize = 1726903;      //֮ǰ��xml�ж�ȡ����1726903����ҳ������� 
float list_1[graphSize], list_2[graphSize];  //�洢������ҳ��weight(��������"weight"ָ��"pagerank")��ֵ 
float *weightList, *tmpWeightList;  //ָ��weight�����ָ�� 
int outSizeList[graphSize];			//outSizeList��ÿ��Ԫ�ش�����Ӧ��ҳ�ĳ����� 
vector<int>* linkList[graphSize];   //graphSize��С��vector���飬ÿ��vector��ʾ�����ӵ�����ҳ����ҳ��

//�Ӵ����е��롰ͼ�� 
void loadGraph()
{
	// 1.��ȡoutSizeList����ÿ����ҳ�ĳ����� 
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
    
	// 2.��ȡlinkList����ÿ����ҳ�����ӵ���� 
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

//����pageRank�ĺ��� 
void pageRank()
{
	float dampingFactor = 0.85;  // ��
	int maxIterations = 100;     // ����������
	float minDelta = 0.0001;      // ȷ�������Ƿ�����Ĳ���
    
	//�Ƚ�ͼ��û�г��ߵĽڵ��Ϊ�����нڵ㶼�г��� ���������С��ڵ㡱���ǡ�ҳ�桱�� 
	//������zeroList�洢����û�г��ߵĽڵ㣬֮���ڵ��������⴦������ 
	vector<int> zeroList;
	for (int i = 0; i < graphSize; ++i)
	{
    		weightList[i] = 1.0 / graphSize;   // Page ��Ȩֵ����ÿ���ڵ㸳���ʼ��weightΪ1 / N
		if (outSizeList[i] == 0)           //���û�г��ߣ��Ͱѽڵ����zeroList�� 
			zeroList.insert(zeroList.end(), i);
	}
        
	float dampingValue = (1.0 - dampingFactor) / graphSize;  // ��ʽ�е�(1-��)/N����
	float change, left;  //change��ʾһ�ε����еĸı�����left��ʾ��ʽ�Ⱥ��ұ��еĲ��� (1-��)/N���ǲ���
	vector<int>::iterator k;
    
	for (int i = 0; i < maxIterations; ++i)
	{
		cout << "Iteration: " << i << endl;
		change = 0;
    	
		//����ͼ�е�ÿ���ڵ� 
		for (int j = 0; j < graphSize; ++j)
		{
    			left = 0;
    		
    			//��ÿ���ڵ㣬left��ʾ��ָ��ýڵ����Щ�ڵ�� weightֵ/������ ֮�� 
			for (k = linkList[j]->begin(); k < linkList[j]->end(); ++k)
				left += weightList[*k] / outSizeList[*k];
    			
			//  ����Ϊ�˽�ʡ�ڴ棬�ٶ�û�г��ߵĽڵ���ָ��ͼ�����нڵ�(�����Լ�)����zeroList�洢
			//��Щû�г��ߵĽڵ㣬Ȼ���ر�����Щ����ڵ㣬���leftҪ������Щ�ڵ�� Ȩֵ/ͼ�нڵ���� 
			for (k = zeroList.begin(); k < zeroList.end(); ++k)
				left += weightList[*k] / graphSize;
			
			//tmpWeightListָ�������洢���ǣ���ͼ��ÿ���ڵ���һ�ֵ����õ����µ�Ȩֵ 
			tmpWeightList[j] = dampingFactor * left + dampingValue;
			
			//�ۼӵ�����ÿ���ڵ�Ȩֵ�ĸı��� 
			change += abs(tmpWeightList[j] - weightList[j]);
		}
		
		//�����ʾһ�ֵ��������󣬸���ͼ�нڵ�Ȩֵ�Ĺ��̣�
		//Ϊ�˼ӿ�����ٶȣ�����ֱ����weightListָ��tmpWeightListָ������飬
		//tmpWeightListָ��weightList֮ǰָ�������
		//�൱�ڰ�tmpWeightList��ֵ����������weightList 
		float *tmp = weightList;
		weightList = tmpWeightList;
		tmpWeightList = tmp;
		
		cout << "Change = " << change << endl;
		//����ı���С��minDelta����ֹ���� 
		if (change < minDelta)
			break;
	}
}

//�����ռ��������뱾�ش��� 
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
	
	//weightListָ��list_1, tmpWeightListָ��list_2 
	weightList = list_1;
	tmpWeightList = list_2;
	
	cout << "start pageRank()" << endl;
	pageRank();
	
	cout << "save the weightList" << endl;
	saveWeightList();
	
	return 0;
} 