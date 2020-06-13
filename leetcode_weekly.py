import requests
from bs4 import BeautifulSoup
import ujson
from multiprocessing import Process,Lock

#周赛
#url_path='https://leetcode-cn.com/contest/api/ranking/weekly-contest-191/?pagination=20&region=local'
#双周赛
#url_path='https://leetcode-cn.com/contest/api/ranking/biweekly-contest-27/?pagination=20&region=local'

#contest_type   周赛类型 1:周赛 2:双周赛
#num_list       周赛场次列表
#usr_id_set     待检索的user_name
#用户信息有"username","user_slug","real_name"三个字段，这里使用“username”，即排名中的“用户名”
class WeeklyContest:
    def __init__(self, contest_type, num_list, usr_id_set):
        self.contest_type = contest_type
        self.contest_num_list = num_list
        self.usr_id_set = usr_id_set
        self.weekly2usr2info = {}

    def get_contest_info(self):
        for contest_num in self.contest_num_list:
            resp = self.get_contest_resp(contest_num, 1)
            if len(resp) == 2:
                #contest_type = "weekly-contest-"
                #if self.contest_type == 2:
                #    contest_type = "biweekly-contest-"
                #contest_type += str(contest_num)
                #print(contest_type, "has no data!")
                continue
            resp_json = ujson.loads(resp)
            #从首页获取用户总数，计算出页数（每页25人）
            user_num = resp_json['user_num']
            page_num = int(user_num / 25)
            if user_num % 25 != 0:
                page_num += 1
            #print("user_num: ", user_num, ", page_num: ", page_num)
            self.weekly2usr2info.setdefault(contest_num, dict())
            usr2info = self.weekly2usr2info[contest_num]
            if self.search_id_from_resp(resp_json, user_num, usr2info) == False:
                for n in range(2, page_num + 1):
                    resp = self.get_contest_resp(contest_num, n)
                    resp_json = ujson.loads(resp)
                    if self.search_id_from_resp(resp_json, user_num, usr2info) == True:
                        break

    def record_data(self):
        #记录数据，可指定分隔符
        for weekly, usr2info in self.weekly2usr2info.items():
            for usr, info in usr2info.items():
                print(",".join([str(self.contest_type), str(weekly), usr] + [str(i) for i in info]))

    #请求http服务，返回string类型的数据
    def get_contest_resp(self, contest_num, page_num):
        type_str = "weekly"
        if self.contest_type == 2:
            type_str = "biweekly"
        url_path='https://leetcode-cn.com/contest/api/ranking/{0[0]}-contest-{0[1]}/?pagination={0[2]}&region=local'.format((type_str, contest_num, page_num))
        resp=requests.get(url_path)
        #resp.encoding='gb2312'
        resp.encoding='utf-8'
        return resp.text

    #返回用户集是否获取完成，完成的话就不需再往后找了
    def search_id_from_resp(self, resp_json, user_num, usr2info):
        total_rank = resp_json["total_rank"]
        for rank in total_rank:
            if rank["username"] in self.usr_id_set:
                #暂时加了一个分数和名次，还需要什么直接往里加
                usr2info[rank["username"]] = [rank["rank"] + 1, user_num, rank["score"]]
                if len(usr2info) == len(self.usr_id_set):
                    return True
        return False

