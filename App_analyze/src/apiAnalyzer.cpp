#include <iostream>
#include <cstring>
#include <map>
#include <vector>
#include <string>
#include <fstream>
#include <algorithm>
#include <time.h>
using namespace std;

class Api
{
public:
	string name; //api的名字
	int cnt; //api被调用的次数
	Api(string name_)
	{
		name = name_;
		cnt = 0;
	}
	bool operator < (const Api& c) const
	{
		return cnt > c.cnt;
	}
};
//不是我想用全局变量的，是因为怕内存不够啊→_→
vector<string> apis;
vector<Api> sum;  //统计调用某个api的app个数
const int maxlinelength = 100000;
char line[maxlinelength];

int getindex(string name);
int main()
{
	time_t starttime, endtime;
	starttime = time(NULL);
	int cnt;
	string eachapp;
	string path = "D:\\mydata\\b_output\\";
	string apicalledpath = path + "apicalled.txt";
	string apipath = path + "api.txt";
	string apifeatpath = path + "apifeat.txt";
	fstream apicalledreader(apicalledpath, ios::in);
	fstream apireader(apipath, ios::in);
	fstream apifeatwriter(apifeatpath, ios::out);

	if (!apicalledreader.is_open() || !apireader.is_open() || !apifeatwriter.is_open())
	{
		cout << "打开文件失败" << endl;
		exit(0);
	}

	cnt = 0;
	while (apicalledreader.getline(line, maxlinelength))
	{
		apis.push_back(line);
		sum.push_back(*(new Api(line))); //构建一下统计表
		cnt++;
	}
	cout << "一共有" << cnt << "种API" << endl;

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

//	map<string, int>::iterator i_;
//	for (i_ = mapping.begin(); i_ != mapping.end(); ++i_)
//		cout << (*i_).first << " " << (*i_).second << endl;

	int offset, index;
	int start, end;
	int num, size;
	cnt = 0;
	while (apireader.getline(line, maxlinelength))
	{
		eachapp = string(line);
		size = eachapp.size();
		//先读数字
		start = eachapp.find(',') + 1;
		end = eachapp.find(',', start);
		num = atoi(eachapp.substr(start, end).c_str());

		//开始读取该app的调用api列表
		start = end + 1;
		for (int i = 0; i < num; i++)
		{
			end = eachapp.find(',', start);
			index = getindex(eachapp.substr(start, end - start));
			if (index == -1)
			{
				cout << "出错了！" << endl;
				system("pause");
				exit(0);
			}
			else
			{
				sum[index].cnt++;
			}
			start = end + 1;
		}
		cnt++;
		eachapp.clear();
	}
	cout << "一共有" << cnt << "种APP" << endl;

	vector<Api>::iterator k;
	sort(sum.begin(), sum.end());
	cnt = 0;
	int filtersize = 9; //这里可以调整一下过滤大小
	for (k = sum.begin(); k != sum.end(); ++k)
	{
		if ((*k).cnt <= filtersize) 
			break;
		cnt++;
		apifeatwriter << (*k).name << ',' << (*k).cnt << endl;;
	}
	cout << "一共有" << cnt << "种被调用次数不少于" << filtersize + 1 << "的api" << endl;

	sum.clear();
	apireader.close();
	apicalledreader.close();
	apifeatwriter.close();

	endtime = time(NULL);
	cout << "一共耗费了" << endtime - starttime << "秒" << endl;
	system("pause");
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