
from multiprocessing import Process, Value, Array
import os, signal, time

# Numero de procesos concurrentes
N_PROCESOS = 5


class Terminator:
    run_forever = True

    def __init__(self):
        signal.signal(signal.SIGTERM, self.handler)

    def handler(self, signum, frame):
        print('Process {}: Signal catched'.format(os.getpid()))
        self.run_forever = False

def P(i, c, t):
    terminator = Terminator()
    print('Proceso {} (PID {}) lanzado!'.format(i, os.getpid()))
    while terminator.run_forever:
        c[i] = 1
        t[i] = max(t) + 1
        c[i] = 0

        print('Proceso {} (PID {}) esperando a entrar en su SC'.format(i, os.getpid()))
        for k in range(N_PROCESOS):
            while c[k] != 0:
                pass
            
            while t[k] != 0 and t[k] < t[i]:
                pass

        # Inicio SC
        print('Proceso {} (PID {}) avanza a su SC'.format(i, os.getpid()))
        time.sleep(5)
        # Fin SC
        print('Proceso {} (PID {}) sale de su SC'.format(i, os.getpid()))

        t[i] = 0
        #...

def main():
    t = Array('i', N_PROCESOS)
    c = Array('i', N_PROCESOS)

    for i in range(N_PROCESOS):
        p = Process(target=P, args=(i, c, t))
        p.start()


if __name__ == "__main__":
    main()