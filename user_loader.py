'''
file : user_loader.py
author : zhenliang153(zhenliang153@163.com)
date : 2020-11-29 19:03:21
brief : 获取用户信息
'''
#import os
#import sys

class UserLoader(object):
    def getUser(self, file):
        users = []
        with open(file, 'r') as user_ids:
            
            for user_id in user_ids:
                user_id = user_id.strip()
                if len(user_id) != 0 and user_id[0] != '#':
                    users.append(user_id)

        return list(set(users))
