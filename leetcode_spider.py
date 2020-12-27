'''
file : leetcode_spider.py
author : zhenliang153(zhenliang153@163.com)
date : 2020-11-29 18:24:27
brief : 获取了LeetCode指定用户在指定场次的排名信息
'''
import configparser
import content_loader
import sys
import time
import user_loader
import webpage_parser

'''
主程序
'''
class LeetCodeSpider(object):
    
    def __init__(self, path):

        config = configparser.ConfigParser()
        config.read(path)

        self.__users = config.get('spider', 'users')
        self.__contents = config.get('spider', 'contents')
        self.__results = config.get('spider', 'contents')
        self.__time_out = int(config.get('spider', 'time_out'))
        self.__thread_count = int(config.get('spider', 'thread_count'))

    def __get_users(self):
        loader = user_loader.UserLoader()
        users = loader.getUser(self.__users)
        return users
        
    def __get_contents(self):
        loader = content_loader.ContentLoader()
        contents = loader.getContent(self.__contents)
        return contents

    def run(self):
        # TODO 添加日志记录模块
        users = self.__get_users()
        print("users :", users)
        contents = self.__get_contents()
        print("weekly :", contents[0])
        print("biweekly :", contents[1])

        parser = webpage_parser.WebpageParser(users, "user_slug")
        contents_info = [dict(), dict()]

        # TODO 开启多线程抓取信息
        for n in contents[0]:
            contents_info[0][n] = {}
            parser.get_content_info(1, n, contents_info[0][n])
        for n in contents[1]:
            contents_info[1][n] = {}
            parser.get_content_info(2, n, contents_info[1][n])

        # TODO 将结果输出到result文件中
        print("周赛成绩 : ")
        print(contents_info[0])
        print("双周赛成绩 : ")
        print(contents_info[1])

def spider_run():
    PATH = './spider.cfg'
    spider = LeetCodeSpider(PATH)
    spider.run()

def main():
    begin_time = time.time()
    spider_run()
    end_time = time.time()
    print("cost: ", str(end_time - begin_time))

if __name__=="__main__":
    sys.exit(main())

