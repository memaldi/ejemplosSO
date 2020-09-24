from multiprocessing import Process, Value, Lock
import os, time, signal

# Numero de procesos concurrentes
N_PROCESOS = 2

class Terminator:
    run_forever = True

    def __init__(self):
        signal.signal(signal.SIGTERM, self.handler)

    def handler(self, signum, frame):
        print('Process {}: Signal catched'.format(os.getpid()))
        self.run_forever = False

# Simulacion de la instruccion hardware testset
def testset(lock, key):
    with lock:
        if key.value == 0:
            key.value = 1
            return True
        else:
            return False


def procedure(lock, i, key):
    terminator = Terminator()
    print('Proceso {} (PID {}) lanzado!'.format(i, os.getpid()))

    while terminator.run_forever:
        # ...
        print('Proceso {} (PID {}) esperando a entrar en su SC'.format(i, os.getpid()))
        while not testset(lock, key):
            pass

        # Inicio SC
        print('Proceso {} (PID {}) avanza a su SC'.format(i, os.getpid()))
        time.sleep(5)
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
