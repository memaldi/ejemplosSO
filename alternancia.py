from multiprocessing import Process, Value
import os, signal, time

# Numero de procesos concurrentes
N_PROCESOS = 2

class Terminator:
    run_forever = True

    def __init__(self):
        signal.signal(signal.SIGTERM, self.handler)

    def handler(self, signum, frame):
        print('Process {}: Signal catched'.format(os.getpid()))
        self.run_forever = False


def P1(i, vab):
    terminator = Terminator()
    print('Proceso {} (PID {}) lanzado!'.format(i, os.getpid()))
    while terminator.run_forever:
        # ...
        print('Proceso {} (PID {}) esperando a entrar en su SC'.format(i, os.getpid()))
        while vab.value == 2:
            pass

        # Inicio SC
        print('Proceso {} (PID {}) avanza a su SC'.format(i, os.getpid()))
        time.sleep(10)
        # Fin SC
        print('Proceso {} (PID {}) sale de su SC'.format(i, os.getpid()))
        vab.value = 2
        # ...


def P2(i, vab):
    terminator = Terminator()
    print('Proceso {} (PID {}) lanzado!'.format(i, os.getpid()))
    while terminator.run_forever:
        # ...
        print('Proceso {} (PID {}) esperando a entrar en su SC'.format(i, os.getpid()))
        while vab.value == 1:
            pass

        # Inicio SC
        print('Proceso {} (PID {}) avanza a su SC'.format(i, os.getpid()))
        time.sleep(10)
        # Fin SC
        print('Proceso {} (PID {}) sale de su SC'.format(i, os.getpid()))
        vab.value = 1
        # ...


def main():
    vab = Value('i', 1)

    p1 = Process(target=P1, args=(1, vab))
    p2 = Process(target=P2, args=(2, vab))

    p1.start()
    p2.start()


if __name__ == "__main__":
    main()