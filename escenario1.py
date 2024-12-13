import simulacion
import simpy
import random
import time

class RobotOptimizado(simulacion.Robot):
    def run(self):
        while True:
            yield self.env.timeout(random.uniform(10, 30))  # Penalizar tiempos de llegada
            simulated_time = random.uniform(self.n * 1, self.n * 2)  # Más lento para tableros grandes
            self.execution_times.append(simulated_time)
            print(f"[RobotOptimizado] Resolviendo {self.n} reinas en {simulated_time:.2f} segundos.")

class HumanoOptimizado(simulacion.Humano):
    def solve_n_queens(self, n):
        board = [-1] * n
        self.place_queen(board, 0)
        return board

def main(n):
    env = simpy.Environment()
    robot = RobotOptimizado(env, n)
    humano = HumanoOptimizado(env, n)
    env.run(until=480)

if __name__ == "__main__":
    n = 8  # Aquí puedes cambiar el valor de n según sea necesario
    main(n)