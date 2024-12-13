import simulacion
import simpy
import random
import time

class InteraccionRobot(simulacion.Robot):
    def run(self):
        while True:
            yield self.env.timeout(random.uniform(10, 30))
            simulated_time = random.uniform(self.n * 0.05, self.n * 0.2)
            self.execution_times.append(simulated_time)
            print(f"[InteraccionRobot] Resolviendo {self.n} reinas en {simulated_time:.2f} segundos.")

    def ask_for_help(self, n):
        return random.choice([True, True, False])

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
        simulated_time = random.uniform(n * 0.8, n * 1.2)  # Simula tiempo humano
        time.sleep(simulated_time / 10)  # Divide el tiempo para evitar largas pausas
        if user_help:
            simulated_time *= 0.2  # Reducir tiempo si hay ayuda
            print(f"[Ayuda] El usuario asistió en la resolución del problema de {n} reinas.")
        return [-1] * n  # Simula un tablero vacío como resultado

def main(n):
    env = simpy.Environment()
    robot = InteraccionRobot(env, n)
    humano = InteraccionHumano(env, n)
    env.run(until=480)

if __name__ == "__main__":
    n = 8
    main(n)