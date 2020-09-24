# Ejemplos de Espera Activa


## Uso

* Lanzar el algoritmo deseado: `python algoritmo.py`. El programa mostrará por pantalla los PID de los procesos en ejecución.
* Si se desea terminar alguno de los procesos para comprobar si se cumple la progresión finita, etc. basta con ejecutar `kill PID` en un terminal.
El proceso capturará la señal `SIGTERM` y finalizará al final del "bucle infinito".