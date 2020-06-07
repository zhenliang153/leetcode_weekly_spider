import time
from multiprocessing import Process,Lock
from leetcode_weekly import WeeklyContest

#获取leetcode-cn周赛成绩，查找指定用户，指定场次
#将待查询场次和用户列表，分别填入num_list和usr_id_set

def taskMain(lock, contest_type, num_list, usr_id_list):
    task = WeeklyContest(contest_type, num_list, usr_id_set)
    task.get_contest_info()
    lock.acquire()
    task.record_data();
    lock.release()

if __name__=="__main__":
    begin_time = time.time()
    
    #周赛场次
    weekly_list = [i for i in range(189, 193)]
    #双周赛场次
    biweekly_list = [i for i in range(25, 28)]

    contest_list = []
    contest_list.append((1, weekly_list))
    contest_list.append((2, biweekly_list))
    
    #将待查询user_name放usr_id_set中
    usr_id_set = { }

    if len(usr_id_set) == 0 or len(contest_list) == 0:
        print("Please add user_name to usr_id_set or init contest_list!")
    else:
        process_list = []
        lock = Lock()
        print(",".join(["Type", "Contest", "User"] + ["Rank", "Total", "Score"]))
        for contest_type, num_list in contest_list:
            p = Process(target=taskMain,args=(lock, contest_type, num_list, usr_id_set,))
            process_list.append(p)
            p.start()
        #阻塞等待，使得能够有效计时
        for p in process_list:
            p.join()

    end_time = time.time()
    print("cost: ", str(end_time - begin_time))

