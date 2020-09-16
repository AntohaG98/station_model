import time
import random
from threading import Thread


class TimeGen(Thread):

    sleeps = [600, 2400, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 600, 2400, 2400, 2400,
              2400, 2400, 2400, 2400, 600, 0, 0, 0, 0, 0, 0, 0, 0, 0, 600, 600,
              600, 2400]

    num_of_people = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 1,
        7: 3.4,
        8: 5.5,
        9: 3.4,
        10: 2,
        11: 1,
        12: 1,
        13: 1,
        14: 1,
        15: 1,
        16: 1,
        17: 1.3,
        18: 1.7,
        19: 2.4,
        20: 1.5,
        21: 1,
        22: 1,
        23: 1
    }

    def __init__(self, provider):
        Thread.__init__(self, target=self.gen_time)
        self.provider = provider
        self.alive = True
        self.sim_time = 18000       # 5 часов

    def hours_minutes(self):
        return self.sim_time//3600, (self.sim_time//60) % 60

    def get_rand_people(self, mu, size):
        train = int(random.normalvariate(mu, 50) * self.num_of_people[self.provider.hours])
        if train > size:
            train = size
        return train

    def _train(self):
        # этот блок описывает события вокруг каждого поезда
        self.provider.no_train = False
        time.sleep(300 * self.provider.speed)
        self.sim_time += 300
        if self.alive:
            self.provider.hours, self.provider.minutes = self.hours_minutes()
            self.provider.people_dict['train_1'] = self.get_rand_people(700, 2000)
            self.provider.people_dict['train_2'] = self.get_rand_people(280, 800)
            self.provider.people_dict['train_3'] = self.get_rand_people(420, 1200)
            self.provider.arriving = True
            time.sleep(300 * self.provider.speed)
            self.sim_time += 300
            if self.alive:
                self.provider.hours, self.provider.minutes = self.hours_minutes()
                self.provider.boarding = True
                time.sleep(600 * self.provider.speed)
                self.sim_time += 600
                if self.alive:
                    self.provider.hours, self.provider.minutes = self.hours_minutes()
                    self.provider.boarding = False
                    self.provider.no_train = True
                    self.provider.left = True

    def gen_time(self):
        while self.alive:
            self.sim_time = 18000
            self.provider.hours, self.provider.minutes = self.hours_minutes()
            # симуляция начинается в 5:00
            self.provider.people_time = True
            for i in range(len(self.sleeps)):
                if not self.alive:
                    break
                time.sleep(self.sleeps[i] * self.provider.speed)
                self.sim_time += self.sleeps[i]
                self.provider.hours, self.provider.minutes = self.hours_minutes()
                self._train()
            self.provider.people_time = False
            if self.alive:
                time.sleep(1800 * self.provider.speed)
            # симуляция заканчивается в 23:30

    def quit(self):
        self.alive = False
