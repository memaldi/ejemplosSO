import time
import random
from multiprocessing import Process, Value, BoundedSemaphore, Queue, Array, Event

N_ESTUDIANTES = 15

def resolverProblema(id_estudiante):
    print("El estudiante {id_estudiante} está resolviendo un problema".format(id_estudiante=id_estudiante))
    time.sleep(random.uniform(0, 10))
    

def encargado(id, s_sala, s_ocupacion, cont_ocupacion, cola_fotocopias, a_estudiante):
    while True:
        id_estudiante, prob_resueltos = cola_fotocopias.get()
        print("El encargado {id} está imprimiendo los {prob_resueltos} problemas del estudiante {id_estudiante}".format(id=id, prob_resueltos=prob_resueltos, id_estudiante=id_estudiante))
        time.sleep(random.uniform(0, 10))
        print("El encargado {id} ha impreso todos los problemas del estudiante {id_estudiante}".format(id=id, id_estudiante=id_estudiante))
        a_estudiante[id_estudiante] = 1

        with s_ocupacion:
            cont_ocupacion.value -= 1
        s_sala.release()

def estudiante(id, s_sala, s_ocupacion, cont_ocupacion, cola_fotocopias, a_estudiante):
    prob_resueltos = 0
    while True:
        resolverProblema(id)
        prob_resueltos += 1
        print("El estudiante {id_estudiante} ha terminado de resolver un problema, problemas resueltos: {prob_resueltos}".format(id_estudiante=id, prob_resueltos=prob_resueltos))
        
        if prob_resueltos >= 5:
            # wait(s_sala)
            s_sala.acquire()
            
            # wait(s_ocupacion)
            with s_ocupacion:
                cont_ocupacion.value += 1
            # signal(s_ocupacion)

            cola_fotocopias.put((id, prob_resueltos))
            while a_estudiante[id] == 0:
                pass
            a_estudiante[id] = 0
            prob_resueltos = 0
                
        else:
            # wait(s_ocupacion)
            s_ocupacion.acquire()
            print("Estudiante {id}, valor cont_ocupacion: {cont_ocupacion}".format(id=id, cont_ocupacion=cont_ocupacion.value))
            if cont_ocupacion.value < 2:
                cont_ocupacion.value += 1
                # signal(s_ocupacion)
                s_ocupacion.release()

                # wait(s_sala)
                s_sala.acquire()

                cola_fotocopias.put((id, prob_resueltos))
                while a_estudiante[id] == 0:
                    pass
                a_estudiante[id] = 0
                prob_resueltos = 0
            else:
                # signal(s_ocupacion)
                s_ocupacion.release()
   

def main():
    s_sala = BoundedSemaphore(2)
    s_ocupacion = BoundedSemaphore(1)
    cont_ocupacion = Value('i', 0)
    cola_fotocopias = Queue()
    a_estudiante = Array('i', N_ESTUDIANTES)

    for i in range(N_ESTUDIANTES):
        p = Process(target=estudiante, args=(i, s_sala, s_ocupacion, cont_ocupacion, cola_fotocopias, a_estudiante))
        p.start()
    
    e1 = Process(target=encargado, args=(1, s_sala, s_ocupacion, cont_ocupacion, cola_fotocopias, a_estudiante))
    e2 = Process(target=encargado, args=(2, s_sala, s_ocupacion, cont_ocupacion, cola_fotocopias, a_estudiante))
    
    e1.start()
    e2.start()

if __name__ == "__main__":
    main()