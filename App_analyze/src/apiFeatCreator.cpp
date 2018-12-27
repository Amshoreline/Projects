#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <vector>
#include <algorithm>
#include <time.h>
using namespace std;

vector<string> apis;
vector<int> apivector;
const int maxlinelength = 100000;
char line[maxlinelength];
int getindex(string name);

int main()
{
	time_t starttime, endtime;
	starttime = time(NULL);
	bool isTrain = true;
	string path = "D:\\mydata\\b_output\\";
	string apipath = path + "api.txt";
	string apifeatpath = path + "apifeat.txt";
	string trainApipath = path + "train\\trainApi.txt";
	string apiVectorpath = path + "train\\apiVector.txt";
	string testApipath = path + "test\\testApi.txt";
	string apiVectorpath2 = path + "test\\apiVector.txt";

	fstream apireader(apipath, ios::in);
	fstream apifeatreader(apifeatpath, ios::in);
	fstream trainApiwriter(trainApipath, ios::out);
	fstream apiVectorwriter(apiVectorpath, ios::out);
	fstream testApiwriter(testApipath, ios::out);
	fstream apiVectorwriter2(apiVectorpath2, ios::out);

	if (!apireader.is_open() || !apifeatreader.is_open() ||
		!trainApiwriter.is_open() || !apiVectorwriter.is_open() ||
		!testApiwriter.is_open() || !apiVectorwriter2.is_open())
	{
		cout << "打开文件失败" << endl;
		system("pause");
		exit(0);
	}
	//先获取api列表
	int cnt = 0, size;
	while (apifeatreader.getline(line, maxlinelength))
	{
		cnt++;
		size = strlen(line);
		int i;
		for (i = 0; i < size; ++i)
		{
			if (line[i] == ',')
				break;
		}
		apis.push_back(string(line).substr(0, i));
	}
	cout << "一共参考了" << cnt << "个API" << endl;
	sort(apis.begin(), apis.end());
	//检查逆序
	vector<string>::iterator i__;
	vector<string>::iterator myend = apis.end();
	myend--;
	for (i__ = apis.begin(); i__ != myend; ++i__)
	{
		if (*i__ > *(i__ + 1))
		{
			cout << "逆序" << endl;
			system("pause");
			exit(0);
		}
	}

	size = apis.size();
	if (isTrain)
		apiVectorwriter << size;
	else
		apiVectorwriter2 << size;
	//读取app的api调用数据

	for (int i = 0; i < size; i++)
		apivector.push_back(0);

	cnt = 0;
	string eachapp, name;
	int start, end, num, index;
	while (apireader.getline(line, maxlinelength))
	{
		for (int i = 0; i < size; i++)
			apivector[i] = 0;

		eachapp = string(line);

		//读名字
		start = 0;
		end = eachapp.find(',');
		name = eachapp.substr(start, end - start);
		//读数字
		start = end + 1;
		end = eachapp.find(',', start);
		num = atoi(eachapp.substr(start, end - start).c_str());
		
		//开始读取该app的调用api列表
		start = end + 1;
		for (int i = 0; i < num; i++)
		{
			end = eachapp.find(',', start);
			index = getindex(eachapp.substr(start, end - start));
			if (index != -1)
			{
				apivector[index] = 1;
			}
			start = end + 1;
		}
		if (isTrain)
			trainApiwriter << name << ',';
		else
			testApiwriter << name << ',';

		for (int i = 0; i < size - 1; i++)
			if (isTrain)
				trainApiwriter << apivector[i] << ',';
			else
				testApiwriter << apivector[i] << ',';
		if (isTrain)
			trainApiwriter << apivector[size - 1] << endl;
		else
			testApiwriter << apivector[size - 1] << endl;

		cnt++;
		eachapp.clear();
	}
	cout << "一共有" << cnt << "个app" << endl;

	apireader.close();
	apifeatreader.close();
	trainApiwriter.close();
	apiVectorwriter.close();
	testApiwriter.close();
	apiVectorwriter2.close();

	endtime = time(NULL);
	cout << "一共耗费了" << endtime - starttime << "秒" << endl;
	system("pause");
	return 0;
}

//二分查找下标
int getindex(string name)
{
	int left = 0, right = apis.size();
	int mid;
	while (left < right)
	{
		mid = (left + right) / 2;
		if (name == apis[mid])
			return mid;
		else if (name < apis[mid])
			right = mid;
		else
			left = mid + 1;
	}
	return -1;
}