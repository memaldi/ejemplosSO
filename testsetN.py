from multiprocessing import Process, Value, Array, Lock

# Numero de procesos concurrentes
N_PROCESOS = 5

def testset(lock, key):
    with lock:
        if key.value == 0:
            key.value = 1
            return True
        else:
            return False


def procedure(lock, i, key, c, N):
    while True:
        # ...
        print('Proceso {} inicia la secuencia'.format(i))
        c[i] = 1
        print('Proceso {} esperando a entrar en su SC'.format(i))
        while (c[i] != 0) and (not testset(lock, key)):
            pass
        c[i] = 0
        
        # Inicio SC
        print('Proceso {} avanza a su SC'.format(i))
        # Fin SC
        print('Proceso {} sale de su SC'.format(i))
        j = (i + 1) % N.value
        print('Proceso {}, j = {} ANTES del while'.format(i, j))
        while (j != i) and (c[j] == 0):
            print('Proceso {}, j = {} DENTRO del while'.format(i, j))
            j = (j + 1) % N.value
        print('Proceso {}, j = {} FUERA del while'.format(i, j))
        if j == i:
            print('Proceso {}, j = {} modifica key'.format(i, j))
            key.value = 0
        else:
            print('Proceso {}, j = {} asigna c[j] = 0'.format(i, j))
            c[j] = 0

def main():
    N = Value('i', N_PROCESOS)
    key = Value('i', 0)
    c = Array('i', N_PROCESOS)

    lock = Lock()
    for i in range(N_PROCESOS):
        Process(target=procedure, args=(lock, i, key, c, N)).start()

if __name__ == "__main__":
    main()

