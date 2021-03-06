import abc
import asyncio
import pprint
import time

# 如果没有比赛则设为时间戳最大值
NO_CONTEST = 2147483647


class Contest(metaclass=abc.ABCMeta):
    def __init__(self):
        self.updated_time = time.time()
        self.list, self.begin_time, self.during_time = [], NO_CONTEST, NO_CONTEST  # 时间全以时间戳为单位
        # 下列时间都是最新未开始的比赛时间
        self.list, self.begin_time, self.during_time = asyncio.run(self.get_contest())

    def get_note_time(self):
        return self.begin_time - 15 * 60

    def get_end_time(self):
        return self.begin_time + self.during_time

    async def update_contest(self, flag=0):  # flag=1代表强制更新
        # 在要求强制更新或者超过上次跟新九个小时后或者上一场已经结束，与main文件中的定时器刷新函数要求的一致
        if int(time.time()) - self.updated_time >= 9 * 3600 or int(
                time.time()) >= self.begin_time + self.during_time or flag == 1:
            self.updated_time = int(time.time())
            self.list, self.begin_time, self.during_time = await self.get_contest()
            print("更新{}比赛成功".format(self.__class__.__name__))
        # return self.info

    def show_all(self):
        print("list : {}\nduring_time : {}\nbegin_time : {}\n update_time : {}".format(self.list, self.during_time,
                                                                                       self.begin_time,
                                                                                       self.updated_time))

    @abc.abstractmethod
    async def get_contest(self):
        pass

    @abc.abstractmethod
    async def get_rating(self, name):
        pass

    async def get_next_contest(self):
        # 如果请求失败就判断时候应当更换比赛信息
        if time.time() > self.get_end_time():
            if len(self.list) > 0:
                del (self.list[0])
                return self.list, self.list[0]['begin_time'], self.list[0]['during_time']
            else:
                return [
                           {
                               "contest_info": "最近没有比赛~",
                               'begin_time': NO_CONTEST,
                               'during_time': NO_CONTEST,
                           }
                       ], NO_CONTEST, NO_CONTEST
        else:
            return self.list, self.list[0]['begin_time'], self.list[0]['during_time']
