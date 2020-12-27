'''
file : webpage_parser.py
author : zhenliang153(zhenliang153@163.com)
date : 2020年12月27日 17:01:58:wq
brief : 爬取网页信息并解析
'''
import requests
import ujson

'''
爬取网页信息并解析
'''
class WebpageParser:

    '''
    @param user_id_set : 待检索的user_id列表
    @param user_identify : user_id在JSON中对应的字段，用户信息有"username","user_slug","real_name"三个字段，这里使用“user_slug”，这也是个性域名的ID
    '''
    def __init__(self, user_id_set, user_identify):
        self.__user_id_set = user_id_set
        # JSON中的用户标识信息
        self.__user_identify = user_identify

    '''
    @brief 根据周赛场次获取用户成绩信息
    @param content_type : 周赛类型 1 周赛 2 双周赛
    @param content_num : 周赛场次
    @param user2info : 出参，返回用户成绩信息
    '''
    def get_content_info(self, content_type, content_num, user2info):

        resp = self.__get_content_resp(content_type, content_num, 1)
        if len(resp) == 2:
            print("ERROR")
            return
        #print(resp)
        resp_json = ujson.loads(resp)
        # 从首页获取用户总数，计算出页数（每页25人）
        user_num = resp_json['user_num']
        page_num = int(user_num / 25)
        if user_num % 25 != 0:
            page_num += 1
        # print("user_num: ", user_num, ", page_num: ", page_num)
        user_id_len = len(self.__user_id_set)
        # 第一页是否已获取完毕？(哪有那么容易进前25名)
        if self.__search_id_from_resp(resp_json, user2info) == False:
            for n in range(2, page_num + 1):
                resp = self.__get_content_resp(content_type, content_num, n)
                resp_json = ujson.loads(resp)
                if self.__search_id_from_resp(resp_json, user2info):
                    break
        for _, info in user2info.items():
            info.append(user_num)


    # 请求http服务，返回string类型的数据
    # 周赛URL示例
    # url_path='https://leetcode-cn.com/content/api/ranking/weekly-content-220/?pagination=20&region=local'
    # 双周赛URL示例
    # url_path='https://leetcode-cn.com/content/api/ranking/biweekly-content-40/?pagination=20&region=local'
    def __get_content_resp(self, content_type, content_num, page_num):
        type_str = "weekly"
        if content_type == 2:
            type_str = "biweekly"
        url_path = 'https://leetcode-cn.com/contest/api/ranking/{0[0]}-contest-{0[1]}/?pagination={0[2]}&region=local'.format((type_str, content_num, page_num))
        print("[url_path]", url_path)
        resp = requests.get(url_path)
        # resp.encoding = 'gb2312'
        resp.encoding = 'utf-8'
        return resp.text

    # 返回用户集是否获取完成，完成的话就不再往后找了
    def __search_id_from_resp(self, resp_json, user2info):
        total_rank = resp_json["total_rank"]
        for rank in total_rank:
            if rank[self.__user_identify] in self.__user_id_set:
                # 暂时加了一个分数和名次，还需要什么直接往里加
                user2info[rank[self.__user_identify]] = [rank["rank"] + 1, rank["score"]]
                if len(user2info) == len(self.__user_id_set):
                    return True
        return False

