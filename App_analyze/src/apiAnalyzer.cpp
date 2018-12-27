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
	string name; //api������
	int cnt; //api�����õĴ���
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
//����������ȫ�ֱ����ģ�����Ϊ���ڴ治������_��
vector<string> apis;
vector<Api> sum;  //ͳ�Ƶ���ĳ��api��app����
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
		cout << "���ļ�ʧ��" << endl;
		exit(0);
	}

	cnt = 0;
	while (apicalledreader.getline(line, maxlinelength))
	{
		apis.push_back(line);
		sum.push_back(*(new Api(line))); //����һ��ͳ�Ʊ�
		cnt++;
	}
	cout << "һ����" << cnt << "��API" << endl;

	//�������
	vector<string>::iterator i__;
	vector<string>::iterator myend = apis.end();
	myend--;
	for (i__ = apis.begin(); i__ != myend; ++i__)
	{
		if (*i__ > *(i__ + 1))
		{
			cout << "����" << endl;
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
		//�ȶ�����
		start = eachapp.find(',') + 1;
		end = eachapp.find(',', start);
		num = atoi(eachapp.substr(start, end).c_str());

		//��ʼ��ȡ��app�ĵ���api�б�
		start = end + 1;
		for (int i = 0; i < num; i++)
		{
			end = eachapp.find(',', start);
			index = getindex(eachapp.substr(start, end - start));
			if (index == -1)
			{
				cout << "�����ˣ�" << endl;
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
	cout << "һ����" << cnt << "��APP" << endl;

	vector<Api>::iterator k;
	sort(sum.begin(), sum.end());
	cnt = 0;
	int filtersize = 9; //������Ե���һ�¹��˴�С
	for (k = sum.begin(); k != sum.end(); ++k)
	{
		if ((*k).cnt <= filtersize) 
			break;
		cnt++;
		apifeatwriter << (*k).name << ',' << (*k).cnt << endl;;
	}
	cout << "һ����" << cnt << "�ֱ����ô���������" << filtersize + 1 << "��api" << endl;

	sum.clear();
	apireader.close();
	apicalledreader.close();
	apifeatwriter.close();

	endtime = time(NULL);
	cout << "һ���ķ���" << endtime - starttime << "��" << endl;
	system("pause");
}
//���ֲ����±�
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