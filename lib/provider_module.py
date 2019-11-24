from threading import Thread


class StationProvider(Thread):

    # daemon = True
    train_capacity = [2000, 800, 1200]

    def __init__(self, main_mod):
        Thread.__init__(self, target=self.main_loop)
        self.main_mod = main_mod
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
        self.arriving = False           # поезд приехал
        self.boarding = False           # началась посадка
        self.no_train = True            # поезд уехал
        self.people_came = False        # пришли новые люди
        self.people_num = 0             # их количество
        self.first = True
        self.left = False
        self.people_time = False
        self.hours = 0
        self.minutes = 0
        self.speed = 1 / 1000            # 100 менять на нужную

    def main_loop(self):
        while self.alive:
            if self.people_came:
                self.people_came_func()
                self.people_came = False
            if self.arriving:
                self.arriving_func()
                self.arriving = False
                self.first = True
            if self.boarding:
                self.boarding_func()
            if self.left:
                print(self.hours, ":", self.minutes,
                      '\nПоезд уехал')
                self.left = False

    def people_came_func(self):
        # обработка новых людей
        if self.no_train:
            wh = round(self.people_num * 0.66)
            p_to_platform = self.people_num - wh
            pl_1 = round(p_to_platform * 0.5)
            pl_2 = round(p_to_platform * 0.2)
            self.people_dict['waiting_hall'] += wh
            self.people_dict['platform_1'] += pl_1
            self.people_dict['platform_2'] += pl_2
            self.people_dict['platform_3'] += p_to_platform - pl_1 - pl_2
        else:
            pl_1 = round(self.people_num * 0.5)
            pl_2 = round(self.people_num * 0.2)
            self.people_dict['platform_1'] += pl_1
            self.people_dict['platform_2'] += pl_2
            self.people_dict['platform_3'] += self.people_num - pl_1 - pl_2
        print(self.hours, ":", self.minutes,
              '\nПришли люди. Загруженность вокзала:'
              '\n     - зал ожидания: ', self.people_dict['waiting_hall'],
              '\n     - платформа 1: ', self.people_dict['platform_1'],
              '\n     - платформа 2: ', self.people_dict['platform_2'],
              '\n     - платформа 3: ', self.people_dict['platform_3']
              )

    def arriving_func(self):
        for i in range(0, 3):
            self.people_dict[''.join(['platform_', str(i + 1)])] += \
                self.people_dict[''.join(['train_', str(i + 1)])]
            self.people_dict[''.join(['people_from_train_', str(i + 1)])] = \
                self.people_dict[''.join(['train_', str(i + 1)])]
            self.people_dict[''.join(['train_', str(i + 1)])] = 0
        print(self.hours, ":", self.minutes,
              '\nПриехали поезда. Люди вышли на платформы:'
              '\n     - поезд 1: ', self.people_dict['people_from_train_1'],
              '\n     - поезд 2: ', self.people_dict['people_from_train_2'],
              '\n     - поезд 3: ', self.people_dict['people_from_train_3']
              )
        print('Загруженность вокзала:'
              '\n     - зал ожидания: ', self.people_dict['waiting_hall'],
              '\n     - платформа 1: ', self.people_dict['platform_1'],
              '\n     - платформа 2: ', self.people_dict['platform_2'],
              '\n     - платформа 3: ', self.people_dict['platform_3']
              )

    def boarding_func(self):
        if self.first:
            for i in range(0, 3):
                # приехавшие люди уходят
                self.people_dict[''.join(['platform_', str(i + 1)])] -= \
                    self.people_dict[''.join(['people_from_train_', str(i + 1)])]
                self.people_dict[''.join(['people_from_train_', str(i + 1)])] = 0
            print(self.hours, ":", self.minutes,
                  '\nЛюди из поездов ушли. Загруженность вокзала:'
                  '\n     - зал ожидания: ', self.people_dict['waiting_hall'],
                  '\n     - платформа 1: ', self.people_dict['platform_1'],
                  '\n     - платформа 2: ', self.people_dict['platform_2'],
                  '\n     - платформа 3: ', self.people_dict['platform_3']
                  )
            # люди из зала идут на платформы
            if self.people_dict['waiting_hall'] != 0:
                pl_1 = round(self.people_dict['waiting_hall'] * 0.5)
                pl_2 = round(self.people_dict['waiting_hall'] * 0.2)
                self.people_dict['platform_1'] += pl_1
                self.people_dict['platform_2'] += pl_2
                self.people_dict['platform_3'] += self.people_dict['waiting_hall'] - pl_1 - pl_2
                self.people_dict['waiting_hall'] = 0
            self.first = False
            print(self.hours, ":", self.minutes,
                  '\nЛюди из зала ожидания пошли на платформы. Загруженность вокзала:'
                  '\n     - зал ожидания: ', self.people_dict['waiting_hall'],
                  '\n     - платформа 1: ', self.people_dict['platform_1'],
                  '\n     - платформа 2: ', self.people_dict['platform_2'],
                  '\n     - платформа 3: ', self.people_dict['platform_3']
                  )
            # люди садятся в поезд
        for i in range(0, 3):
            if self.people_dict[''.join(['platform_', str(i + 1)])] != 0:
                free = self.train_capacity[i] - self.people_dict[''.join(['train_', str(i + 1)])]
                if free != 0:
                    if self.people_dict[''.join(['platform_', str(i + 1)])] <= free:
                        self.people_dict[''.join(['train_', str(i + 1)])] += \
                            self.people_dict[''.join(['platform_', str(i + 1)])]
                        self.people_dict[''.join(['platform_', str(i + 1)])] = 0
                    else:
                        self.people_dict[''.join(['train_', str(i + 1)])] += free
                        self.people_dict[''.join(['platform_', str(i + 1)])] -= free
                    print('Посадка. Загруженность вокзала:'
                          '\n     - платформа 1: ', self.people_dict['platform_1'],
                          '\n     - платформа 2: ', self.people_dict['platform_2'],
                          '\n     - платформа 3: ', self.people_dict['platform_3'],
                          '\n     - поезд 1: ', self.people_dict['train_1'],
                          '\n     - поезд 2: ', self.people_dict['train_2'],
                          '\n     - поезд 3: ', self.people_dict['train_3']
                          )
