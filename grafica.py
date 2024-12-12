import matplotlib.pyplot as plt
import numpy as np
import time
import random
from simulacion import Robot, Humano

def simulate_algorithm_times(n_values, runs=10):
    las_vegas_times = []
    determinista_times = []

    for n in n_values:
        # Simulación para el algoritmo Las Vegas
        lv_exec_times = []
        for _ in range(runs):
            robot = Robot()
            start_time = time.time()
            robot.solve_n_queens(n, method='las_vegas')
            lv_exec_times.append(time.time() - start_time)
        
        # Simulación para el algoritmo determinista
        det_exec_times = []
        for _ in range(runs):
            humano = Humano()
            start_time = time.time()
            humano.solve_n_queens(n)
            det_exec_times.append(time.time() - start_time)
        
        # Promediar tiempos
        las_vegas_times.append(np.mean(lv_exec_times))
        determinista_times.append(np.mean(det_exec_times))

    return las_vegas_times, determinista_times

def plot_graph(n_values, las_vegas_times, determinista_times):
    plt.figure(figsize=(10, 5))
    plt.plot(n_values, las_vegas_times, marker='o', label='Las Vegas', color='blue')
    plt.plot(n_values, determinista_times, marker='o', label='Determinista', color='red')
    plt.title('Comparación de Tiempos de Ejecución: Algoritmo Las Vegas vs Algoritmo Determinista')
    plt.xlabel('Tamaño del Tablero (n)')
    plt.ylabel('Tiempo de Ejecución (segundos)')
    plt.xticks(n_values)
    plt.legend()
    plt.grid(True)
    plt.savefig('tiempos_ejecucion.png')  # Guardar la gráfica como archivo PNG
    plt.show()

def main():
    n_values = [4, 5, 6, 8, 10, 12, 15]
    las_vegas_times, determinista_times = simulate_algorithm_times(n_values)
    plot_graph(n_values, las_vegas_times, determinista_times)

if __name__ == "__main__":
    main()
