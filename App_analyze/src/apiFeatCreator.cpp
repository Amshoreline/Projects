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
		cout << "���ļ�ʧ��" << endl;
		system("pause");
		exit(0);
	}
	//�Ȼ�ȡapi�б�
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
	cout << "һ���ο���" << cnt << "��API" << endl;
	sort(apis.begin(), apis.end());
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

	size = apis.size();
	if (isTrain)
		apiVectorwriter << size;
	else
		apiVectorwriter2 << size;
	//��ȡapp��api��������

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

		//������
		start = 0;
		end = eachapp.find(',');
		name = eachapp.substr(start, end - start);
		//������
		start = end + 1;
		end = eachapp.find(',', start);
		num = atoi(eachapp.substr(start, end - start).c_str());
		
		//��ʼ��ȡ��app�ĵ���api�б�
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
	cout << "һ����" << cnt << "��app" << endl;

	apireader.close();
	apifeatreader.close();
	trainApiwriter.close();
	apiVectorwriter.close();
	testApiwriter.close();
	apiVectorwriter2.close();

	endtime = time(NULL);
	cout << "һ���ķ���" << endtime - starttime << "��" << endl;
	system("pause");
	return 0;
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