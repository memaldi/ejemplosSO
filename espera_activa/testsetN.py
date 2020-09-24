from multiprocessing import Process, Value, Array, Lock
import time, os, signal

# Numero de procesos concurrentes
N_PROCESOS = 5

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


def procedure(lock, i, key, c):
    terminator = Terminator()
    print('Proceso {} (PID {}) lanzado!'.format(i, os.getpid()))

    while terminator.run_forever:
        # ...
        c[i] = 1
        print('Proceso {} (PID {}) esperando a entrar en su SC'.format(i, os.getpid()))
        while (c[i] != 0) and (not testset(lock, key)):
            pass
        c[i] = 0
        
        # Inicio SC
        print('Proceso {} (PID {}) avanza a su SC'.format(i, os.getpid()))
        time.sleep(5)
        # Fin SC
        print('Proceso {} (PID {}) sale de su SC'.format(i, os.getpid()))
        j = (i + 1) % N_PROCESOS
       
        while (j != i) and (c[j] == 0):
            print('Proceso {} (PID {}), j = {} DENTRO del while'.format(i, os.getpid(), j))
            j = (j + 1) % N_PROCESOS
        
        print('Proceso {} (PID {}), j = {} FUERA del while'.format(i, os.getpid(), j))
        if j == i:
            print('Proceso {} (PID {}), j = {} modifica key'.format(i, os.getpid(), j))
            key.value = 0
        else:
            print('Proceso {i} (PID {pid}), j = {j} asigna c[{j}] = 0'.format(i=i, pid=os.getpid(), j=j))
            c[j] = 0

def main():
    key = Value('i', 0)
    c = Array('i', N_PROCESOS)

    lock = Lock()
    for i in range(N_PROCESOS):
        Process(target=procedure, args=(lock, i, key, c)).start()

if __name__ == "__main__":
    main()

