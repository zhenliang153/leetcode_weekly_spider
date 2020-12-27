'''
file : content_loader.py
author : zhenliang153(zhenliang153@163.com)
date : 2020-11-29 19:21:38
brief : 获取周赛场次信息
'''
#import os
#import sys

class ContentLoader(object):

    def getContent(self, file):
        #print("file : " , file)
        type2index = {}
        type2index["weekly"] = 0
        type2index["biweekly"] = 1

        contents = []
        for i in range(len(type2index)):
            contents.append([])
        index = -1
        with open(file, 'r') as lines:
            for line in lines:
                line = line.strip()
                if len(line) == 0 or line[0] == '#':
                    continue
                if len(line) > 2 and line[0] == '[' and line[-1] == ']':
                    key = line[1:-1]
                    if key not in type2index:
                        print("ERROR key : ", key)
                    else:
                        index = type2index[key]
                    continue
                if index == -1:
                    print("ERROR index : -1")
                    continue
                
                # Format : 218-220,221
                segment = line.split(',')
                for s in segment:
                    v = s.split('-')
                    if len(v) == 1:
                        contents[index].append(int(v[0]))
                    elif len(v) == 2:
                        for i in range(int(v[0]), int(v[1]) + 1):
                            contents[index].append(i)
                    else:
                        print("ERROR segment : ", s)

        # 去重
        for i in range(len(contents)):
            contents[i] = list(set(contents[i]))

        return contents
