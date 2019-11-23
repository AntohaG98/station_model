import time


class TimeGen:

    def __init__(self, speed):
        self.speed = 1 / speed  # например если speed = 10, то симуляция в 10 раз быстрее реального времени
        self.arriving_soon = False  # 5 минут до поезда
        self.arriving = False  # поезд приехал
        self.boarding = False  # началась посадка
        self.left = False  # поезд уехал

    def _train(self):
        # этот блок описывает события вокруг каждого поезда
        self.arriving_soon = True
        time.sleep(300 * self.speed)
        self.arriving = True
        time.sleep(300 * self.speed)
        self.boarding = True
        time.sleep(600 * self.speed)
        self.left = True

    def gen_time(self):
        # симуляция начинается в 5:00
        time.sleep(600 * self.speed)
        self._train()
        time.sleep(2400 * self.speed)
        for _ in range(10):
            self._train()
        time.sleep(600 * self.speed)
        self._train()
        for _ in range(7):
            time.sleep(2400 * self.speed)
            self._train()
        time.sleep(600 * self.speed)
        self._train()
        for _ in range(9):
            self._train()
        for _ in range(3):
            time.sleep(600 * self.speed)
            self._train()
        time.sleep(2400 * self.speed)
        self._train()
        time.sleep(1800 * self.speed)
        # симуляция заканчивается в 23:30
