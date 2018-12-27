#include <iostream>
#include <cstring>
#include <fstream>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <time.h>
using namespace std;

string readApiLines(string line);
set<string> allapis;

int main()
{
	time_t start, end;
	start = time(NULL);

	const int maxLineLength = 50000;
	vector<string> whitelist;
	set<string> apis;
	
	string path = "D:\\mydata\\b_output\\";

	string apiPath = path + "apilist_for_apk\\";
	string whitePath =  path + "white.txt"; //��
	string newwhitePath = path + "newwhite.txt";
	string outputPath = path + "api.txt";
	string apicalledPath = path + "apicalled.txt";

	fstream fout(outputPath, ios::out);
	fstream readWhite(whitePath, ios::in);
	fstream writeWhite(newwhitePath, ios::out);
	fstream writeapi(apicalledPath, ios::out);

	if (!readWhite.is_open() || !fout.is_open() | !writeWhite.is_open())
	{
		cout << "���ļ�����";
		system("pause");
		exit(0);
	}

	int length = 0;
	char line[maxLineLength];
	while (readWhite.getline(line, maxLineLength))
	{
		whitelist.insert(whitelist.end(), line);
		length++;
	}
	cout << "whitelistһ��" << length << "��" << endl;
	//��ȡwhitelist
	fstream fread;
	vector<string>::iterator i;
	vector<string>::iterator j;
	int n = 0; //����д���˼���Ӧ��
	for (i = whitelist.begin(); i != whitelist.end(); i++)
	{
		fread.open(apiPath + *i + ".apk.txt", ios::in);
		if (!fread.is_open())
		{
			cout << "�Ҳ���ָ���ļ�:" << endl;
			cout << apiPath + *i + ".apk.txt"<< endl;
			system("pause");
			exit(0);
		}
		int linecnt = 0;
		while (fread.getline(line, maxLineLength))
		{
			//���˿���
			if (strlen(line) > 1)
			{
				linecnt++;
				string apiName = readApiLines(line);
				apis.insert(apiName);
				allapis.insert(apiName);
			}
		}
		if (linecnt <= 1)
		{
			cout << *i << "ֻ��" << linecnt << "��" << endl;
			j = i;
			j--;
			whitelist.erase(i);
			i = j;
			apis.clear();
			fread.close();
			continue;
		}
		n++;
	//	cout << "API�ļ�һ��" << linecnt << "��" << endl;
		//��ȡapis��д��fout
		fout << *i << ',';
		set<string>::iterator k;
		int cnt = apis.size();
		fout << cnt << ',';
		for (k = apis.begin(); k != apis.end(); ++k)
		{
			fout << *k << ',';
		}
		//cout << whitelist[i] << "������" << cnt << "��API" << endl;
		fout << endl;

		apis.clear();
		fread.close();
	}
	cout << "д����" << n << "��Ӧ������" << endl;
	cout << "һ����" << allapis.size() << "��API" << endl;
	set<string>::iterator k;
	for (k = allapis.begin(); k != allapis.end(); ++k)
		writeapi << *k << endl;
	//����whitelist
	for (i = whitelist.begin(); i != whitelist.end(); ++i)
		writeWhite << *i << endl;

	readWhite.close();
	writeWhite.close();
	fout.close();

	end = time(NULL);
	cout << "�ķ���" << end - start << "��";
	system("pause");
}
string readApiLines(string line)
{
	int start = line.find("android");
	int end = line.find(' ', start);
	if (start < end)
		return line.substr(start, end - start);
	else
		return " ";
}