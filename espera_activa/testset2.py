from multiprocessing import Process, Value, Lock
import os

# Numero de procesos concurrentes
N_PROCESOS = 2


def testset(lock, key):
    with lock:
        if key.value == 0:
            key.value = 1
            return True
        else:
            return False


def procedure(lock, i, key):
    while True:
        # ...
        while not testset(lock, key):
            pass

        # Inicio SC
        print('Proceso {} (PID {}) avanza a su SC'.format(i, os.getpid()))
        # Fin SC
        print('Proceso {} (PID {}) sale de su SC'.format(i, os.getpid()))

        key.value = 0
        # ...


def main():
    key = Value('i', 0)

    lock = Lock()
    for i in range(N_PROCESOS):
        p = Process(target=procedure, args=(lock, i, key))
        p.start()


if __name__ == "__main__":
    main()
