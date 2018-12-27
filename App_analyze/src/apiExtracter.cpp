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
	string whitePath =  path + "white.txt"; //读
	string newwhitePath = path + "newwhite.txt";
	string outputPath = path + "api.txt";
	string apicalledPath = path + "apicalled.txt";

	fstream fout(outputPath, ios::out);
	fstream readWhite(whitePath, ios::in);
	fstream writeWhite(newwhitePath, ios::out);
	fstream writeapi(apicalledPath, ios::out);

	if (!readWhite.is_open() || !fout.is_open() | !writeWhite.is_open())
	{
		cout << "打开文件错误";
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
	cout << "whitelist一共" << length << "行" << endl;
	//读取whitelist
	fstream fread;
	vector<string>::iterator i;
	vector<string>::iterator j;
	int n = 0; //计算写入了几个应用
	for (i = whitelist.begin(); i != whitelist.end(); i++)
	{
		fread.open(apiPath + *i + ".apk.txt", ios::in);
		if (!fread.is_open())
		{
			cout << "找不到指定文件:" << endl;
			cout << apiPath + *i + ".apk.txt"<< endl;
			system("pause");
			exit(0);
		}
		int linecnt = 0;
		while (fread.getline(line, maxLineLength))
		{
			//过滤空行
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
			cout << *i << "只有" << linecnt << "行" << endl;
			j = i;
			j--;
			whitelist.erase(i);
			i = j;
			apis.clear();
			fread.close();
			continue;
		}
		n++;
	//	cout << "API文件一共" << linecnt << "行" << endl;
		//读取apis并写入fout
		fout << *i << ',';
		set<string>::iterator k;
		int cnt = apis.size();
		fout << cnt << ',';
		for (k = apis.begin(); k != apis.end(); ++k)
		{
			fout << *k << ',';
		}
		//cout << whitelist[i] << "调用了" << cnt << "个API" << endl;
		fout << endl;

		apis.clear();
		fread.close();
	}
	cout << "写入了" << n << "个应用数据" << endl;
	cout << "一共有" << allapis.size() << "种API" << endl;
	set<string>::iterator k;
	for (k = allapis.begin(); k != allapis.end(); ++k)
		writeapi << *k << endl;
	//更新whitelist
	for (i = whitelist.begin(); i != whitelist.end(); ++i)
		writeWhite << *i << endl;

	readWhite.close();
	writeWhite.close();
	fout.close();

	end = time(NULL);
	cout << "耗费了" << end - start << "秒";
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