import time
from threading import Thread
from lib.gen_people_module import PeopleGenerator


class StationProvider(Thread):

    # daemon = True
    train_capacity = [2000, 800, 1200]

    def __init__(self):
        Thread.__init__(self, target=self.main_loop)
        self.gen_people_thread = PeopleGenerator(self)
        self.alive = True
        self.people_dict = {
            'waiting_hall': 0,
            'platform_1': 0,
            'platform_2': 0,
            'platform_3': 0,
            'train_1': 0,           # значение обновляется, когда приезжает поезд и пополняется
            'train_2': 0,           # по ходу его наполнения, когда поезд уезжает, значение обнуляется
            'train_3': 0,
            'people_from_train_1': 0,
            'people_from_train_2': 0,
            'people_from_train_3': 0
        }
        self.arriving_soon = False      # 5 минут до поезда
        self.arriving = False           # поезд приехал
        self.boarding = False           # началась посадка
        self.no_train = True            # поезд уехал
        self.people_came = False        # пришли новые люди
        self.people_num = 0             # их количество
        self.first = True

        self.start()

    def main_loop(self):
        while self.alive:
            if self.people_came:
                self.people_came_func()
            if self.arriving:
                self.arriving_func()
            if self.boarding:
                self.boarding_func()

    def people_came_func(self):
        # обработка новых людей
        if self.no_train:
            self.people_dict['waiting_hall'] += round(self.people_num * 0.66)
            p_to_platform = self.people_num - self.people_dict['waiting_hall']
            self.people_dict['platform_1'] += round(p_to_platform * 0.5)
            self.people_dict['platform_2'] += round(p_to_platform * 0.2)
            self.people_dict['platform_3'] += \
                p_to_platform - self.people_dict['platform_1'] - self.people_dict['platform_2']
        else:
            self.people_dict['platform_1'] += round(self.people_num * 0.5)
            self.people_dict['platform_2'] += round(self.people_num * 0.2)
            self.people_dict['platform_3'] += \
                self.people_num - self.people_dict['platform_1'] - self.people_dict['platform_2']

    def arriving_func(self):
        for i in range(0, 3):
            self.people_dict[''.join(['platform_', str(i + 1)])] += \
                self.people_dict[''.join(['train_', str(i + 1)])]
            self.people_dict[''.join(['people_from_train_', str(i + 1)])] = \
                self.people_dict[''.join(['train_', str(i + 1)])]
            self.people_dict[''.join(['train_', str(i + 1)])] = 0
        self.arriving = False
        self.first = True

    def boarding_func(self):
        for i in range(0, 3):
            if self.first:
                # приехавшие люди уходят
                self.people_dict[''.join(['platform_', str(i + 1)])] -= \
                    self.people_dict[''.join(['people_from_train_', str(i + 1)])]
                self.people_dict[''.join(['people_from_train_', str(i + 1)])] = 0
                # люди из зала идут на платформы
                if self.people_dict['waiting_hall'] != 0:
                    self.people_dict['platform_1'] += round(self.people_dict['waiting_hall'] * 0.5)
                    self.people_dict['platform_2'] += round(self.people_dict['waiting_hall'] * 0.2)
                    self.people_dict['platform_3'] += \
                        self.people_dict['waiting_hall'] - self.people_dict['platform_1'] - \
                        self.people_dict['platform_2']
                    self.people_dict['waiting_hall'] = 0
                self.first = False
            # люди садятся в поезд
            free = self.train_capacity[i] - self.people_dict[''.join(['train_', str(i + 1)])]
            if free != 0:
                if self.people_dict[''.join(['platform_', str(i + 1)])] <= free:
                    self.people_dict[''.join(['train_', str(i + 1)])] += \
                        self.people_dict[''.join(['platform_', str(i + 1)])]
                    self.people_dict[''.join(['platform_', str(i + 1)])] = 0
                else:
                    self.people_dict[''.join(['train_', str(i + 1)])] += free
                    self.people_dict[''.join(['platform_', str(i + 1)])] -= free
