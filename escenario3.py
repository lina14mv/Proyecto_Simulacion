import simulacion
import simpy
import random
import time

class InteraccionRobot(simulacion.Robot):
    def run(self):
        while True:
            yield self.env.timeout(random.uniform(10, 30))
            start_time = time.time()
            user_help = self.ask_for_help(self.n)
            self.solve_n_queens(self.n, method='las_vegas', user_help=user_help)
            self.execution_time = time.time() - start_time
            print(f"[Interacción Robot] Resolviendo {self.n} reinas en {self.execution_time:.2f} segundos.")
            break

    def ask_for_help(self, n):
        return random.choice([True, False])

    def solve_n_queens(self, n, method='las_vegas', user_help=False):
        solutions = []
        attempts = 0
        while not solutions and attempts < 100:
            board = self.generate_random_board(n)
            if self.backtrack(board, 0):
                solutions.append(board)
            attempts += 1

            if user_help:
                print(f"[Ayuda] El usuario asistió en la resolución del problema de {n} reinas.")
        return solutions

class InteraccionHumano(simulacion.Humano):
    def run(self):
        while True:
            yield self.env.timeout(random.uniform(10, 30))
            start_time = time.time()
            user_help = self.ask_for_help(self.n)
            self.solve_n_queens(self.n, user_help=user_help)
            self.execution_time = time.time() - start_time
            self.execution_times.append(self.execution_time)
            print(f"[Interacción Humano] Resolviendo {self.n} reinas en {self.execution_time:.2f} segundos.")

    def ask_for_help(self, n):
        return random.choice([True, False])

    def solve_n_queens(self, n, user_help=False):
        board = [-1] * n
        self.place_queen(board, 0)
        if user_help:
            print(f"[Ayuda] El usuario asistió en la resolución del problema de {n} reinas.")
        return board

def main():
    env = simpy.Environment()
    robot = InteraccionRobot(env, 8)
    humano = InteraccionHumano(env, 8)
    env.run(until=480)

if __name__ == "__main__":
    main()