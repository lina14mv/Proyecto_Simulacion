import simulacion
import simpy
import random
import time

class RobotBonificado(simulacion.Robot):
    def run(self):
        total_bonus = 0
        while True:
            yield self.env.timeout(random.uniform(10, 30))
            start_time = time.time()
            self.solve_n_queens(self.n, method='las_vegas')
            self.execution_time = time.time() - start_time
            
            if self.execution_time < 5:
                bonus = 10
                total_bonus += bonus
                print(f"[Robot Bonificado] Resolviendo {self.n} reinas en {self.execution_time:.2f} segundos. Bonificación total: {total_bonus}")
            break

class HumanoBonificado(simulacion.Humano):
    def run(self):
        total_bonus = 0
        while True:
            yield self.env.timeout(random.uniform(10, 30))
            start_time = time.time()
            self.solve_n_queens(self.n)
            self.execution_time = time.time() - start_time
            self.execution_times.append(self.execution_time)
            if self.execution_time < 5:
                bonus = 10
                total_bonus += bonus
                print(f"[Humano Bonificado] Resolviendo {self.n} reinas en {self.execution_time:.2f} segundos. Bonificación total: {total_bonus}")

def main():
    env = simpy.Environment()
    robot = RobotBonificado(env, 8)
    humano = HumanoBonificado(env, 8)
    env.run(until=480)

if __name__ == "__main__":
    main()