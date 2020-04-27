from time import sleep

from PyQt5.QtCore import *

DataSize = 30
BufferSize = 9
ps = QSemaphore(BufferSize)
ds = QSemaphore(0)
cs = QSemaphore(0)

class Producer(QThread) :
    def run(self):
        for i in range(DataSize):
            ps.acquire()
            print('P')
            sleep(1)
            ds.release()

class Consumer(QThread) :
    def run(self):
        for i in range(DataSize):
            cs.acquire()
            print('C')
            sleep(1)
            ps.release()

class Deliver(QThread) :
    def run(self):
        for i in range(DataSize):
            ds.acquire()
            print('D')
            sleep(1)
            cs.release()

class Goverment(QThread) :
    def run(self):
        for i in range(DataSize):
            # ds.acquire()
            print('G')
            sleep(1)
            # cs.release()

if __name__ == '__main__':
    p = Producer()
    d = Deliver()
    c = Consumer()
    g = Goverment()
    p.start()
    d.start()
    c.start()
    # g.start()
    p.wait()
    d.wait()
    c.wait()
    # g.wait()