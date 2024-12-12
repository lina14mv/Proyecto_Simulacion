import simpy
import random
import time
import numpy as np

class Robot:
    def __init__(self, env, n):
        self.env = env
        self.n = n
        self.execution_times = []
        self.action = env.process(self.run())

    def run(self):
        while True:
            yield self.env.timeout(random.uniform(10, 30))
            start_time = time.time()
            self.solve_n_queens(self.n, method='las_vegas')
            execution_time = time.time() - start_time
            self.execution_times.append(execution_time)
            print(f"[Robot] Resolviendo {self.n} reinas en {execution_time:.2f} segundos.")

    def solve_n_queens(self, n, method='las_vegas'):
        solutions = []
        attempts = 0
        while not solutions and attempts < 100:
            board = self.generate_random_board(n)
            if self.backtrack(board, 0):
                solutions.append(board)
            attempts += 1
        return solutions

    def generate_random_board(self, n):
        return [random.randint(0, n-1) for _ in range(n)]

    def backtrack(self, board, row):
        if row == len(board):
            return True
        for col in range(len(board)):
            if self.is_safe(board, row, col):
                board[row] = col
                if self.backtrack(board, row + 1):
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
        self.execution_times = []
        self.action = env.process(self.run())

    def run(self):
        while True:
            yield self.env.timeout(random.uniform(10, 30))
            start_time = time.time()
            self.solve_n_queens(self.n)
            execution_time = time.time() - start_time
            self.execution_times.append(execution_time)
            print(f"[Humano] Resolviendo {self.n} reinas en {execution_time:.2f} segundos.")

    def solve_n_queens(self, n):
        board = [-1] * n
        self.place_queen(board, 0)
        return board

    def place_queen(self, board, row):
        if row == len(board):
            return True
        for col in range(len(board)):
            if self.is_safe(board, row, col):
                board[row] = col
                if self.place_queen(board, row + 1):
                    return True
        return False

    def is_safe(self, board, row, col):
        for i in range(row):
            if board[i] == col or \
               board[i] - i == col - row or \
               board[i] + i == col + row:
                return False
        return True

def ejecutar_simulacion(n, escenario):
    env = simpy.Environment()
    if escenario == 1:
        from escenario1 import RobotOptimizado as Robot
        from escenario1 import HumanoOptimizado as Humano
    elif escenario == 2:
        from escenario2 import RobotBonificado as Robot
        from escenario2 import HumanoBonificado as Humano
    elif escenario == 3:
        from escenario3 import InteraccionRobot as Robot
        from escenario3 import InteraccionHumano as Humano
    else:
        raise ValueError("Escenario no válido")

    robot = Robot(env, n)
    humano = Humano(env, n)
    env.run(until=480)  # 8 horas en minutos

    robot_times = robot.execution_times
    humano_times = humano.execution_times

    return robot_times, humano_times