import requests
from bs4 import BeautifulSoup
import ujson
import time

#获取leetcode-cn周赛成绩，查找指定用户，指定场次

#周赛
#url_path='https://leetcode-cn.com/contest/api/ranking/weekly-contest-191/?pagination=20&region=local'
#双周赛
#url_path='https://leetcode-cn.com/contest/api/ranking/biweekly-contest-27/?pagination=20&region=local'

#用户信息有"username","user_slug","real_name"三个字段，这里使用“username”，即排名中的“用户名”
usr_id_set = {''}
#周赛场次
weekly_list = [i for i in range(190,192)]
#双周赛场次
biweekly_list = [i for i in range(25,28)]

#请求http服务，返回string类型的数据
def get_contest(weekly_num,page_num, weekly_type):
    type_str = "weekly"
    if weekly_type == 2:
        type_str = "biweekly"
    url_path='https://leetcode-cn.com/contest/api/ranking/{0[0]}-contest-{0[1]}/?pagination={0[2]}&region=local'.format((type_str,weekly_num,page_num))
    resp=requests.get(url_path)
    #resp.encoding='gb2312'
    resp.encoding='utf-8'
    return resp.text

#返回用户集是否获取完成，完成的话就不需再往后找了
def search_id_from_resp(resp_json, usr_id_set, user_num, usr2info):
    total_rank = resp_json["total_rank"]
    for rank in total_rank:
        if rank["username"] in usr_id_set:
            #暂时加了一个分数和名次，还需要什么直接往里加
            usr2info[rank["username"]] = [rank["rank"]+1,user_num,rank["score"]]
            if len(usr2info) == len(usr_id_set):
                return True
    return False
    
#请求周赛数据，weekly_type: 1 周赛 2 双周赛
def get_weekly_info(weekly_num_list, weekly_type):
    weekly2usr2info = {}
    for weekly_num in weekly_num_list:
        resp = get_contest(weekly_num, 1, weekly_type)
        resp_json = ujson.loads(resp)
        #print(resp_json['user_num'])
        #从首页获取用户总数，计算出页数（每页25人）
        user_num = resp_json['user_num']
        page_num = int(user_num / 25)
        if user_num % 25 != 0:
            page_num += 1
        #print("page_num:", page_num)
        weekly2usr2info.setdefault(weekly_num, dict())
        usr2info = weekly2usr2info[weekly_num]
        if search_id_from_resp(resp_json, usr_id_set, user_num, usr2info) == False:
            for n in range(2, page_num + 1):
                resp = get_contest(weekly_num, n, weekly_type)
                resp_json = ujson.loads(resp)
                if search_id_from_resp(resp_json, usr_id_set, user_num, usr2info) == True:
                    break
    #记录数据，可指定分隔符
    for weekly,usr2info in weekly2usr2info.items():
        for usr,info in usr2info.items():
            print(",".join([str(weekly_type), str(weekly), usr] + [str(i) for i in info]))

if __name__=="__main__":
    begin_time = time.time()
    print(",".join(["Type", "Contest", "User"] + ["Rank", "Total", "Score"]))
    get_weekly_info(weekly_list, 1)
    get_weekly_info(biweekly_list, 2)
    end_time = time.time()
    print("cost: ", str(end_time - begin_time))
