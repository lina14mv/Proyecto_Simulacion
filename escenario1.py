import simulacion
import simpy
import random
import time

class RobotOptimizado(simulacion.Robot):
    def solve_n_queens(self, n, method='las_vegas'):
        solutions = []
        attempts = 0
        while not solutions and attempts < 100:
            board = self.generate_random_board(n)
            if self.backtrack(board, 0):
                solutions.append(board)
            attempts += 1
        return solutions

class HumanoOptimizado(simulacion.Humano):
    def solve_n_queens(self, n):
        board = [-1] * n
        self.place_queen(board, 0)
        return board

def main():
    env = simpy.Environment()
    robot = RobotOptimizado(env, 8)
    humano = HumanoOptimizado(env, 8)
    env.run(until=480)

if __name__ == "__main__":
    main()