from multiprocessing import Process, Value
import os, signal

# Numero de procesos concurrentes
N_PROCESOS = 2



def P1(i, vab):
    while True:
        # ...
        while vab.value == 2:
            pass

        # Inicio SC
        print('Proceso {} (PID {}) avanza a su SC'.format(i, os.getpid()))
        # Fin SC
        print('Proceso {} (PID {}) sale de su SC'.format(i, os.getpid()))
        vab.value = 2
        # ...


def P2(i, vab):
    while True:
        # ...
        while vab.value == 1:
            pass

        # Inicio SC
        print('Proceso {} (PID {}) avanza a su SC'.format(i, os.getpid()))
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