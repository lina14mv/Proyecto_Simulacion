import simpy
import random
import time
import numpy as np

class Robot:
    def __init__(self, env, n):
        self.env = env
        self.n = n
        self.execution_times = []  # Lista para almacenar los tiempos de ejecución simulados
        self.action = env.process(self.run()) # Inicia el proceso del robot en el entorno

    def run(self):
        """
        Proceso principal del robot. Simula la solución del problema de las N reinas
        y registra los tiempos de ejecución.
        """
        while True:
            yield self.env.timeout(random.uniform(10, 30))  # Llegada del robot
            start_time = time.time() # Inicia el cronómetro del robot
            self.solve_n_queens(self.n, method='las_vegas') #Resuelve el problema de las N reinas  con las vegas
            execution_time = time.time() - start_time
            # Simular tiempo basado en complejidad la vegas
            simulated_time = random.uniform(self.n * 1.5, self.n * 2.5)
            self.execution_times.append(simulated_time) # Registra el tiempo simulado
            print(f"[Robot] Resolviendo {self.n} reinas en {simulated_time:.2f} segundos.")

    def solve_n_queens(self, n, method='las_vegas'):
        """
        Resuelve el problema de las N reinas utilizando un método aleatorio (Las Vegas).
        :param n: Tamaño del tablero.
        :param method: Método de resolución (por defecto 'las_vegas').
        :return: Lista de soluciones encontradas.
        """
        solutions = []
        attempts = 0
        while not solutions and attempts < 100: # Máximo 100 intentos
            board = self.generate_random_board(n)  # Genera un tablero inicial aleatorio
            if self.backtrack(board, 0): # Intenta resolver usando backtracking
                solutions.append(board)
            attempts += 1
        return solutions

    def generate_random_board(self, n):
        """
        Genera un tablero inicial aleatorio.
        :param n: Tamaño del tablero.
        :return: Lista representando las posiciones de las reinas.
        """
        return [random.randint(0, n-1) for _ in range(n)]

    def backtrack(self, board, row):
        """
        Método de backtracking para resolver el problema.
        :param board: Configuración del tablero actual.
        :param row: Fila actual a procesar.
        :return: True si se encuentra una solución, False en caso contrario.
        """
        if row == len(board): # Si se alcanzó la última fila, es una solución válida
            return True
        for col in range(len(board)):
            if self.is_safe(board, row, col): # Verifica si la posición es segura
                board[row] = col
                if self.backtrack(board, row + 1): # Intenta resolver para la siguiente fila
                    return True
        return False

    def is_safe(self, board, row, col):
        """
        Verifica si es seguro colocar una reina en una posición específica.
        :param board: Configuración actual del tablero.
        :param row: Fila de la posición.
        :param col: Columna de la posición.
        :return: True si es seguro, False en caso contrario.
        """
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
        """
        Proceso principal del humano. Simula la solución del problema de las N reinas
        y registra los tiempos de ejecución.
        """
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
        """
        Resuelve el problema de las N reinas utilizando backtracking.
        :param n: Tamaño del tablero.
        :return: Configuración final del tablero.
        """
        board = [-1] * n
        self.place_queen(board, 0) # Intenta colocar las reinas
        return board

    def place_queen(self, board, row):
        """
        Coloca reinas en el tablero utilizando backtracking.
        :param board: Configuración actual del tablero.
        :param row: Fila actual a procesar.
        :return: True si se encuentra una solución, False en caso contrario.
        """
        if row == len(board): # Si se alcanzó la última fila, es una solución válida
            return True
        for col in range(len(board)):
            if self.is_safe(board, row, col): # Verifica si la posición es segura
                board[row] = col
                if self.place_queen(board, row + 1): # Intenta resolver para la siguiente fila
                    return True
        return False

    def is_safe(self, board, row, col):
        """
        Verifica si es seguro colocar una reina en una posición específica.
        :param board: Configuración actual del tablero.
        :param row: Fila de la posición.
        :param col: Columna de la posición.
        :return: True si es seguro, False en caso contrario.
        """
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True

def ejecutar_simulacion(n, escenario):
    """
    Ejecuta una simulación del escenario seleccionado.
    :param n: Tamaño del tablero.
    :param escenario: Número del escenario a simular.
    :return: Tiempos de ejecución de robot y humano.
    """
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

    # Crea instancias de Robot y Humano
    robot = Robot(env, n)
    humano = Humano(env, n)
    env.run(until=480)  # 8 horas en minutos

    # Obtiene los tiempos de ejecución de ambos
    robot_times = robot.execution_times
    humano_times = humano.execution_times
    
    print (f"Tiempo total simulado: {env.now} minutos")

    return robot_times, humano_times