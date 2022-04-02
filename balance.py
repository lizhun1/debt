'''
COPYRIGHT (C) 2021, lizhun, Fudan University
lizhun    email:21212020102@m.fudan.edu.cn
Fudan University        www.fudan.edu.cn              
-----------------------------------------
Descripttion: this is a program to help me caculate the debt between roommates.
version: 1.0
Author: lizhun
Date: 2022-03-28 19:12:59
LastEditors: lizhun
LastEditTime: 2022-04-02 21:26:38
'''
import argparse
import string
import logging
import sys
class person:
    def __init__(self, name):
        self.name = name
        self.cost_list = []
        self.sum = 0
    def add_cost(self, cost):
        self.cost_list.append(cost)
        self.sum += cost
    def show_list(self):
        for i in range(len(self.cost_list)):
            print(self.cost_list[i])
class balance:
    def __init__(self, person_num,balance_name):
        self.person_num = person_num
        self.balance_name = balance_name
        self.person_dict = {}
    def read_name(self):
        '''
        read name from keyboard
        '''
        self.name = []
        for i in range(self.person_num):
            self.name.append(input("please input name: "))
        for name in self.name:
            self.person_dict[name] = person(name)
    def show_name(self):
        print("person_num is "+str(self.person_num))
        for i in range(self.person_num):
            print(self.name[i])  
    def init_from_file(self,filename):
        self.name = []
        file = open(filename, "r")
        tmp=file.readline()[:-1]
        tmp=tmp.split(":")

        if len(tmp)>1:
            self.balance_name=tmp[1]
            logging.info("balance_name:"+self.balance_name)
        else:
            logging.error("balance_name is not found")

        tmp=file.readline()[:-1]
        tmp=tmp.split(":")
        if tmp[0]=="person_num":
            self.person_num=int(tmp[1])
        else:
            logging.error("person_num is not found")
        tmp=file.readline()[:-1]
        tmp=tmp.split(":")
        if tmp[0]=="name_list":
            tmp=tmp[1].split(" ")
            for i in range(len(tmp)):
                self.name.append(tmp[i])
                logging.info("name is "+tmp[i])
                self.person_dict[tmp[i]] = person(tmp[i])
        else:
            logging.error("name_list is not found")
        logging.info("balance head init success")
        while(True):
            tmp=file.readline()[:-1]
            if tmp=="":
                break
            tmp=tmp.split(":")
            print(tmp)
            self.person_dict[tmp[0]].add_cost(float(tmp[1]))
        logging.info("cost load success")

    def calculate_debt_linear(self):
        '''
        平均分配
        '''
        if len(self.name)==0:
            logging.error("name is empty")
            return
        if len(self.name)==1:
            logging.error("name is only one")
            return
        if len(self.name)>=2:
            for front in self.person_dict:
                for back in self.person_dict:
                    if front==back:
                        continue
                    else:
                        money=self.person_dict[back].sum/len(self.name)-self.person_dict[front].sum/len(self.name)
                        print(front+" pay "+back+" "+str(money if money>0 else 'Nothing'))
            logging.info("calculate success")
        pass
    def write_to_file(self,filename):
        file = open(filename, "w")
        file.write("balance_name:"+self.balance_name+ "\n")
        file.write("person_num:"+str(self.person_num) + "\n")
        file.write("name_list: ")
        for i in range(self.person_num):
            file.write(self.name[i] + " ")
        
        for person in self.person_dict:
            file.write("\n"+person+":"+str(self.person_dict[person].sum))
        file.write("\n")
        file.close()
def get_parser():
    parser = argparse.ArgumentParser(description='balance')
    parser.add_argument('-f','--file',help='the file to be parsed')
    parser.add_argument('-n','--new',help='create a new balance file')
    parser.add_argument('-o','--out',help='the file to write')
    parser.add_argument('-i','--cost',help='add list to file')
    parser.add_argument('-c','--cac',help='caculate the debt')
    return parser
def main():
    parser = get_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    if parser.parse_args().file:
        balance_name = parser.parse_args().file
        balance_obj = balance(0,balance_name)
        balance_obj.init_from_file(balance_name)
        balance_obj.calculate_debt_linear()
    if parser.parse_args().out:
        out_file=parser.parse_args().out
        balance_obj.write_to_file(out_file)
    pass
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    main()
    # bal=balance(3,'test')
    # bal.init_from_file("balance.txt")
    # bal.calculate_debt_linear()
    # bal.show_name()
    # bal.write_to_file('test.txt')