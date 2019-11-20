import time
from threading import Thread


class StationProvider(Thread):

    # daemon = True

    def __init__(self):
        Thread.__init__(self, target=self.main_loop)
        self.alive = True

    def main_loop(self):
        while self.alive:

            time.sleep(2)


s = StationProvider()
s.start()
