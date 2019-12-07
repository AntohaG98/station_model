import random
import time
from threading import Thread


class PeopleGenerator(Thread):

    num_of_people = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0.3,
        6: 1,
        7: 1.7,
        8: 2,
        9: 2.2,
        10: 1.7,
        11: 1,
        12: 1,
        13: 1,
        14: 1,
        15: 1,
        16: 1,
        17: 2,
        18: 3,
        19: 5,
        20: 3,
        21: 2,
        22: 0.7,
        23: 0.5
    }

    def __init__(self, provider, time_gen):
        Thread.__init__(self, target=self.generate)
        self.provider = provider
        self.time_gen = time_gen
        self.alive = True
        self.sim_time = 18000

    def generate(self):
        while self.alive:
            if self.provider.people_time and self.alive:
                self.provider.people_num = int(random.normalvariate(500, 50) * self.num_of_people[self.provider.hours])
                self.provider.people_came = True
                if self.alive:
                    time.sleep(600 * self.provider.speed)
                    self.sim_time += 600
                    self.provider.hours, self.provider.minutes = self.sim_time//3600, (self.sim_time//60) % 60

    def quit(self):
        self.alive = False
