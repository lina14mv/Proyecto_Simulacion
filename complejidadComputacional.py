import simpy
import random
import time
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

class Robot:
    def __init__(self, env, n):
        self.env = env
        self.n = n
        self.execution_times = []  # Lista para almacenar los tiempos de ejecución simulados
        self.action = env.process(self.run()) # Inicia el proceso del robot en el entorno

    def run(self):
        while True:
            yield self.env.timeout(random.uniform(10, 30))  # Llegada del robot
            start_time = time.time() # Inicia el cronómetro del robot
            self.solve_n_queens(self.n, method='las_vegas') # Resuelve el problema de las N reinas con Las Vegas
            execution_time = time.time() - start_time
            # Simular tiempo basado en complejidad Las Vegas
            simulated_time = random.uniform(self.n * 1.5, self.n * 2.5)
            self.execution_times.append(simulated_time) # Registra el tiempo simulado
            print(f"[Robot] Resolviendo {self.n} reinas en {simulated_time:.2f} segundos.")

    def solve_n_queens(self, n, method='las_vegas'):
        solutions = []
        attempts = 0
        while not solutions and attempts < 100: # Máximo 100 intentos
            board = self.generate_random_board(n)  # Genera un tablero inicial aleatorio
            if self.backtrack(board, 0): # Intenta resolver usando backtracking
                solutions.append(board)
            attempts += 1
        return solutions

    def generate_random_board(self, n):
        return [random.randint(0, n-1) for _ in range(n)]

    def backtrack(self, board, row):
        if row == len(board): # Si se alcanzó la última fila, es una solución válida
            return True
        for col in range(len(board)):
            if self.is_safe(board, row, col): # Verifica si la posición es segura
                board[row] = col
                if self.backtrack(board, row + 1): # Intenta resolver para la siguiente fila
                    return True
        return False

    def is_safe(self, board, row, col):
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True

class Humano:
    def __init__(self, env, n):
        self.env = env
        self.n = n
        self.execution_times = [] # Lista para almacenar los tiempos de ejecución simulados
        self.action = env.process(self.run()) # Inicia el proceso del humano en el entorno

    def run(self):
        while True:
            yield self.env.timeout(random.uniform(10, 30))  # Tiempo entre intentos
            start_time = time.time()
            self.solve_n_queens(self.n)
            execution_time = time.time() - start_time
            # Simular tiempo basado en complejidad determinista
            simulated_time = random.uniform(self.n, self.n * 1.5)
            self.execution_times.append(simulated_time)
            print(f"[Humano] Resolviendo {self.n} reinas en {simulated_time:.2f} segundos.")

    def solve_n_queens(self, n):
        board = [-1] * n
        self.place_queen(board, 0) # Intenta colocar las reinas
        return board

    def place_queen(self, board, row):
        if row == len(board): # Si se alcanzó la última fila, es una solución válida
            return True
        for col in range(len(board)):
            if self.is_safe(board, row, col): # Verifica si la posición es segura
                board[row] = col
                if self.place_queen(board, row + 1): # Intenta resolver para la siguiente fila
                    return True
        return False

    def is_safe(self, board, row, col):
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True

def ejecutar_simulacion(n, escenario, repeticiones=10):
    robot_times = []
    humano_times = []

    for _ in range(repeticiones):
        env = simpy.Environment()
        if escenario == 1:
            from escenario1 import RobotOptimizado as Robot
            from escenario1 import HumanoOptimizado as Humano
        elif escenario == 2:
            from escenario2 import RobotBonificado as Robot
            from escenario2 import HumanoOptimizado as Humano
        elif escenario == 3:
            from escenario3 import InteraccionRobot as Robot
            from escenario3 import InteraccionHumano as Humano
        else:
            raise ValueError("Escenario no válido")

        robot = Robot(env, n)
        humano = Humano(env, n)
        env.run(until=(28800/2))  # 4 horas en segundos

        robot_times.extend(robot.execution_times)
        humano_times.extend(humano.execution_times)

    avg_robot_time = np.mean(robot_times)
    avg_humano_time = np.mean(humano_times)

    print(f"Promedio de tiempos de ejecución para n={n}, escenario={escenario}:")
    print(f"Robot: {avg_robot_time:.2f} segundos")
    print(f"Humano: {avg_humano_time:.2f} segundos")

    return avg_robot_time, avg_humano_time

def ajustar_complejidad(valores_n, tiempos_robot, tiempos_humano):
    def f_linear(n, a, b):
        return a * n + b

    def f_quadratic(n, a, b, c): # n = valores_n, a = tiempos_robot, b = tiempos_robot, c = termino constante
        return a * n**2 + b * n + c

    def f_exponential(n, a, b):
        return a * np.exp(b * n)

    valores_n = np.array(valores_n)  # Asegurarse de que valores_n sea un array de numpy
    tiempos_robot = np.array(tiempos_robot)  # Asegurarse de que tiempos_robot sea un array de numpy
    tiempos_humano = np.array(tiempos_humano)  # Asegurarse de que tiempos_humano sea un array de numpy

    params_linear_robot, _ = curve_fit(f_linear, valores_n, tiempos_robot)
    params_quadratic_robot, _ = curve_fit(f_quadratic, valores_n, tiempos_robot)
    params_exponential_robot, _ = curve_fit(f_exponential, valores_n, tiempos_robot)

    params_linear_humano, _ = curve_fit(f_linear, valores_n, tiempos_humano)
    params_quadratic_humano, _ = curve_fit(f_quadratic, valores_n, tiempos_humano)
    params_exponential_humano, _ = curve_fit(f_exponential, valores_n, tiempos_humano)

    plt.scatter(valores_n, tiempos_robot, label='Datos Robot')
    plt.plot(valores_n, f_linear(valores_n, *params_linear_robot), label='Ajuste Lineal Robot')
    plt.plot(valores_n, f_quadratic(valores_n, *params_quadratic_robot), label='Ajuste Cuadrático Robot')
    plt.plot(valores_n, f_exponential(valores_n, *params_exponential_robot), label='Ajuste Exponencial Robot')
    plt.xlabel('Tamaño del Tablero (n)')
    plt.ylabel('Tiempo de Ejecución Promedio (segundos)')
    plt.legend()
    plt.show()

    plt.scatter(valores_n, tiempos_humano, label='Datos Humano')
    plt.plot(valores_n, f_linear(valores_n, *params_linear_humano), label='Ajuste Lineal Humano')
    plt.plot(valores_n, f_quadratic(valores_n, *params_quadratic_humano), label='Ajuste Cuadrático Humano')
    plt.plot(valores_n, f_exponential(valores_n, *params_exponential_humano), label='Ajuste Exponencial Humano')
    plt.xlabel('Tamaño del Tablero (n)')
    plt.ylabel('Tiempo de Ejecución Promedio (segundos)')
    plt.legend()
    plt.show()
    
    # Gráfico de barras para comparar tiempos de ejecución
    bar_width = 0.35
    index = np.arange(len(valores_n))

    plt.figure(figsize=(10, 5))
    plt.bar(index, tiempos_robot, bar_width, label='Robot', color='blue')
    plt.bar(index + bar_width, tiempos_humano, bar_width, label='Humano', color='red')
    plt.xlabel('Tamaño del Tablero (n)')
    plt.ylabel('Tiempo de Ejecución Promedio (segundos)')
    plt.title('Comparación de Tiempos de Ejecución Promedio: Robot vs Humano')
    plt.xticks(index + bar_width / 2, valores_n)
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    valores_n = [4, 5, 6, 8, 10, 12, 15]
    escenario = 1  # Cambiar según el escenario que se quiera probar
    tiempos_robot = []
    tiempos_humano = []

    for n in valores_n:
        avg_robot_time, avg_humano_time = ejecutar_simulacion(n, escenario)
        tiempos_robot.append(avg_robot_time)
        tiempos_humano.append(avg_humano_time)

    ajustar_complejidad(valores_n, tiempos_robot, tiempos_humano)