#include <iostream>
#include <cstring>
#include <string>
#include <fstream>
using namespace std;

const int maxlinelength = 100000;
char line[maxlinelength];
int main()
{
	
	string testPath = "D:\\mydata\\apilist\\testlist.txt";
	string whitePath = "D:\\mydata\\apilist\\white.txt";
	fstream fin(testPath, ios::in);
	fstream fout(whitePath, ios::out);
	if (!fin.is_open() || !fout.is_open())
	{
		cout << "���ļ�����" << endl;
		system("pause");
		exit(0);
	}
	string readline;
	int cnt = 0;
	while (fin.getline(line, maxlinelength))
	{
		cnt++;
		readline = (string)line;
		fout << readline.substr(readline.find(":::") + 3) << endl;
	}
	cout << "���Լ��Ĵ�С��" << cnt << endl;
	system("pause");
}