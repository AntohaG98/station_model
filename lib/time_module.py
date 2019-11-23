import time


class TimeGen:

    def __init__(self, speed):
        self.speed = 1 / speed  # например если speed = 10, то симуляция в 10 раз быстрее реального времени
        self.arriving_soon = False  # 5 минут до поезда
        self.arriving = False  # поезд приехал
        self.boarding = False  # началась посадка
        self.left = False  # поезд уехал
        self.sim_time = 18000  # 5 часов

    sleeps = [600, 2400, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 600, 2400, 2400, 2400,
              2400, 2400, 2400, 2400, 600, 0, 0, 0, 0, 0, 0, 0, 0, 0, 600, 600,
              600, 2400]

    def _train(self):
        # этот блок описывает события вокруг каждого поезда
        self.arriving_soon = True
        time.sleep(300 * self.speed)
        self.sim_time += 300
        self.arriving = True
        time.sleep(300 * self.speed)
        self.sim_time += 300
        self.boarding = True
        time.sleep(600 * self.speed)
        self.sim_time += 600
        self.left = True

    def gen_time(self):
        # симуляция начинается в 5:00
        for i in range(len(self.sleeps)):
            time.sleep(self.sleeps[i] * self.speed)
            self.sim_time += self.sleeps[i]
            self._train()
        time.sleep(1800 * self.speed)
        # симуляция заканчивается в 23:30
