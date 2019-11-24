from lib.provider_module import StationProvider
from lib.gen_people_module import PeopleGenerator
from lib.time_module import TimeGen
# гуй вынесу потом в отдельный модуль


class Gui:

    def __init__(self):
        self.station_provider = StationProvider(self)
        self.people_gen = PeopleGenerator(self.station_provider)
        self.time_gen = TimeGen(self.station_provider)
        self.station_provider.start()
        self.people_gen.start()
        self.time_gen.start()


g = Gui()
