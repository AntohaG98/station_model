import tkinter
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from lib.provider_module import StationProvider
from lib.gen_people_module import PeopleGenerator
from lib.time_module import TimeGen


class Gui:

    speed_dict = {
        "1x": 1/100,
        "2x": 1/200,
        "5x": 1/500,
        "7x": 1/700,
        "10x": 1/1000
    }

    def __init__(self):
        self.root = tkinter.Tk()
        self.time_label = None
        self.info_label = None
        self.wait_num = None
        self.pl_1 = None
        self.pl_2 = None
        self.pl_3 = None
        self.train_1 = None
        self.train_2 = None
        self.train_3 = None
        self.speed = None
        self.save_to_file = None
        self.pause_image = None
        self.wait_image = None
        self.file_var = tkinter.BooleanVar()
        self.window()

        self.station_provider = StationProvider(self)
        self.time_gen = TimeGen(self.station_provider)
        self.people_gen = PeopleGenerator(self.station_provider)

        self.station_provider.start()
        self.time_gen.start()
        self.people_gen.start()

        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.mainloop()

    def window(self):
        self.root.geometry('600x350')
        self.root.config(bg='lavender')
        self.root.title("Модель ЖД вокзала")

        info_frame = tkinter.Frame(self.root, width=580, height=30, bg='lavender')
        info_frame.grid(row=0, column=0, columnspan=3, sticky='w', padx=10, pady=10)

        waiting_frame = tkinter.Frame(self.root, width=160, height=200, bg='lavender')
        waiting_frame.grid(row=2, column=0, sticky='w', padx=10, pady=10)

        train_frame = tkinter.Frame(self.root, width=220, height=200, bg='lavender')
        train_frame.grid(row=2, column=1, sticky='w', padx=10, pady=10)

        control_frame = tkinter.Frame(self.root, width=160, height=200, bg='lavender')
        control_frame.grid(row=2, column=2, sticky='w', padx=10, pady=10)

        # Информационное табло (время и информация о поезде)
        self.time_label = tkinter.Label(info_frame, text='5:00', width=5, relief=tkinter.GROOVE, bg='snow',
                                        bd=2, font='arial 14')
        self.time_label.pack(side='left')

        self.info_label = tkinter.Label(info_frame, text='Начало симуляции', bg='snow',
                                        width=35, relief=tkinter.GROOVE, bd=2, font='arial 14')
        self.info_label.pack(side='left', padx=10)

        # self.pause_image = ImageTk.PhotoImage(Image.open("play.png"))
        # pause_but = tkinter.Button(info_frame, image=self.pause_image, bg='snow', relief=tkinter.GROOVE, bd=2)
        # pause_but.pack(side='right', padx=10, fill="both", expand="yes")

        # Зал ожидания
        wait_label = tkinter.Label(waiting_frame, text='Зал ожидания', width=20, bg='lavender')
        wait_label.pack(side='top')
        self.wait_num = tkinter.Label(waiting_frame, text='0', width=12, height=10, relief=tkinter.GROOVE, bd=2,
                                      bg='snow', font='arial 14')
        self.wait_num.pack(side='top', pady=2)

        # Платформы
        pl1_label = tkinter.Label(train_frame, text='Платформа 1', bg='lavender')
        pl1_label.grid(row=0, column=0, sticky='w')
        self.pl_1 = tkinter.Label(train_frame, text='0', width=20, relief=tkinter.GROOVE, bd=2,
                                  bg='snow', font='arial 14')
        self.pl_1.grid(row=1, column=0, sticky='w', pady=2)
        self.train_1 = tkinter.Label(train_frame, width=20, bg='lavender', font='arial 14')
        self.train_1.grid(row=2, column=0, sticky='w', pady=2)

        pl2_label = tkinter.Label(train_frame, text='Платформа 2', bg='lavender')
        pl2_label.grid(row=3, column=0, sticky='w')
        self.pl_2 = tkinter.Label(train_frame, text='0', width=20, relief=tkinter.GROOVE, bd=2,
                                  bg='snow', font='arial 14')
        self.pl_2.grid(row=4, column=0, sticky='w', pady=2)
        self.train_2 = tkinter.Label(train_frame, width=20, bg='lavender', font='arial 14')
        self.train_2.grid(row=5, column=0, sticky='w', pady=2)

        pl3_label = tkinter.Label(train_frame, text='Платформа 1', bg='lavender')
        pl3_label.grid(row=6, column=0, sticky='w')
        self.pl_3 = tkinter.Label(train_frame, text='0', width=20, relief=tkinter.GROOVE, bd=2,
                                  bg='snow', font='arial 14')
        self.pl_3.grid(row=7, column=0, sticky='w', pady=2)
        self.train_3 = tkinter.Label(train_frame, width=20, bg='lavender', font='arial 14')     # navy
        self.train_3.grid(row=8, column=0, sticky='w', pady=2)

        # Управляющий блок
        speed_label = tkinter.Label(control_frame, text='Скорость', bg='lavender')
        speed_label.grid(row=0, column=0, sticky='w', pady=2)
        speed_values = [u"1x", u"2x", u"5x", u"7x", u"10x"]
        self.speed = tkinter.ttk.Combobox(control_frame, values=speed_values)
        self.speed.set(u"1x")
        self.speed.bind('<<ComboboxSelected>>', self.speed_changed)
        self.speed.grid(row=1, column=0, sticky='w', pady=2)
        self.save_to_file = tkinter.Checkbutton(control_frame, text='Сохранять в файл',
                                                variable=self.file_var, bg='lavender')
        self.save_to_file.grid(row=2, column=0, sticky='w', pady=10)

        empty_label = tkinter.Label(control_frame, text='', bg='lavender', height=10)
        empty_label.grid(row=3, column=0, sticky='w', pady=2)

    def speed_changed(self, event=None):
        self.station_provider.speed = self.speed_dict[self.speed.get()]

    def quit(self):
        self.time_gen.quit()
        self.people_gen.quit()
        self.station_provider.quit()
        self.root.quit()


gui = Gui()
