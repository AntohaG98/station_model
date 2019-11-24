import time
from threading import Thread


class TimeGen(Thread):

    sleeps = [600, 2400, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 600, 2400, 2400, 2400,
              2400, 2400, 2400, 2400, 600, 0, 0, 0, 0, 0, 0, 0, 0, 0, 600, 600,
              600, 2400]

    def __init__(self, provider):
        Thread.__init__(self, target=self.gen_time)
        self.provider = provider
        self.alive = True
        self.sim_time = 18000       # 5 часов

    def hours_minutes(self):
        return self.sim_time//3600, (self.sim_time//60) % 60

    def _train(self):
        # этот блок описывает события вокруг каждого поезда
        self.provider.no_train = False
        time.sleep(300 * self.provider.speed)
        self.sim_time += 300
        self.provider.hours, self.provider.minutes = self.hours_minutes()
        # print('поезд приехал', self.provider.hours, ":", self.provider.minutes)
        self.provider.arriving = True
        time.sleep(300 * self.provider.speed)
        self.sim_time += 300
        self.provider.hours, self.provider.minutes = self.hours_minutes()
        # print('посадка', self.provider.hours, ":", self.provider.minutes)
        self.provider.boarding = True
        time.sleep(600 * self.provider.speed)
        self.sim_time += 600
        self.provider.hours, self.provider.minutes = self.hours_minutes()
        # print('поезд уехал', self.provider.hours, ":", self.provider.minutes)
        self.provider.boarding = False
        self.provider.no_train = True
        self.provider.left = True

    def gen_time(self):
        while self.alive:
            self.sim_time = 18000
            self.provider.hours, self.provider.minutes = self.hours_minutes()
            # print(self.provider.hours, ":", self.provider.minutes)
            # симуляция начинается в 5:00
            self.provider.people_time = True
            for i in range(len(self.sleeps)):
                time.sleep(self.sleeps[i] * self.provider.speed)
                self.sim_time += self.sleeps[i]
                self.provider.hours, self.provider.minutes = self.hours_minutes()
                # print('5 минут до поезда', self.provider.hours, ":", self.provider.minutes)
                self._train()
            self.provider.people_time = False
            time.sleep(1800 * self.provider.speed)
            # симуляция заканчивается в 23:30
