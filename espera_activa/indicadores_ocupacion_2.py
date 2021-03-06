
from multiprocessing import Process, Value
import os, signal, time


class Terminator:
    run_forever = True

    def __init__(self):
        signal.signal(signal.SIGTERM, self.handler)

    def handler(self, signum, frame):
        print('Process {}: Signal catched'.format(os.getpid()))
        self.run_forever = False

def P1(i, c1, c2):
    terminator = Terminator()
    print('Proceso {} (PID {}) lanzado!'.format(i, os.getpid()))
    while terminator.run_forever:
        # ...
        c1.value = 0
        print('Proceso {} (PID {}) esperando a entrar en su SC'.format(i, os.getpid()))
        while c2.value == 0:
            pass
        
        # Inicio SC
        print('Proceso {} (PID {}) avanza a su SC'.format(i, os.getpid()))
        time.sleep(5)
        # Fin SC
        print('Proceso {} (PID {}) sale de su SC'.format(i, os.getpid()))

        c1.value = 1
        #...

def P2(i, c1, c2):
    terminator = Terminator()
    print('Proceso {} (PID {}) lanzado!'.format(i, os.getpid()))
    while terminator.run_forever:
        # ...
        c2.value = 0
        print('Proceso {} (PID {}) esperando a entrar en su SC'.format(i, os.getpid()))
        while c1.value == 0:
            pass
        
        # Inicio SC
        print('Proceso {} (PID {}) avanza a su SC'.format(i, os.getpid()))
        time.sleep(5)
        # Fin SC
        print('Proceso {} (PID {}) sale de su SC'.format(i, os.getpid()))

        c2.value = 1
        #...

def main():
    c1 = Value('i', 1)
    c2 = Value('i', 1)

    p1 = Process(target=P1, args=(1, c1, c2))
    p2 = Process(target=P2, args=(2, c1, c2))

    p1.start()
    p2.start()


if __name__ == "__main__":
    main()