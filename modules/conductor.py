import time
from threading import Lock, Thread

from observable import Observable


class Conductor:

    def __init__(self):
        self.bpm = 90
        self.q = 1/self.bpm*60
        self.started = False
        self.lock = Lock()
        self.obs = Observable()
        self.interval = 0
        self.base_note = 0
        self.last_note = 0
        self.arpeggio_speed = 1
        self.arpeggio_length = 0
        self.arpeggio_step = 0
        self.arpeggio_repeat = True
        self.lastTick = time.time()

    def __start(self):
        if self.started:
            print ("already started")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def stop(self):
        # self.started = False
        self.thread.join()

    def update(self):
        while self.started:
            if self.arpeggio_step > self.arpeggio_length or self.arpeggio_length == 0:
                continue
            if time.time() - self.lastTick > self.q * self.arpeggio_speed:
                self.lastTick = time.time()
                # Go to the next arpeggio
                self.last_note += self.interval * 4
                self.arpeggio_step += 1
                if self.arpeggio_step > self.arpeggio_length:
                    self.last_note = self.base_note
                    if self.arpeggio_repeat:
                        self.arpeggio_step = 0
                    else:
                        continue
                self.obs.trigger('note', self.last_note)

    def play(self, tone):
        if not self.started:
            self.__start()
        self.lastTick = time.time()
        self.base_note = tone
        self.last_note = tone
        self.arpeggio_step = 0
        self.obs.trigger('note', self.last_note)


    def set_bpm(self, bpm):
        self.bpm = bpm
        self.q = 1/self.bpm*60

if __name__ == "__main__" :
    conductor = Conductor()
    conductor.interval = 5
    conductor.arpeggio_length = 3
    conductor.arpeggio_repeat = False

    conductor.obs.on('note', print)
    conductor.play(0)

    time.sleep(1)
    conductor.play(3)
    conductor.arpeggio_repeat = True