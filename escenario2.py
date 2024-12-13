import simpy
import random

class RobotBonificado:
    def __init__(self, env, n):
        self.env = env
        self.n = n
        self.execution_times = []
        self.total_bonus = 0
        env.process(self.run())

    def solve_n_queens(self, n, method='las_vegas'):
        # Simula el tiempo que tarda en resolver el problema de las N-reinas
        simulated_time = random.uniform(n * 0.6, n * 0.9)
        return simulated_time

    def run(self):
         # Método que ejecuta el ciclo de resolución del problema
        while True:
            # Simula un tiempo entre intentos
            yield self.env.timeout(random.uniform(10, 30))
            start_time = self.env.now
            execution_time = self.solve_n_queens(self.n) # Simula el tiempo real
            yield self.env.timeout(execution_time)  # Simula el tiempo real
            self.execution_times.append(execution_time) # Almacena el tiempo de ejecución

            # Bonificación si es rápido
            if execution_time < 5:
                bonus = 10
                self.total_bonus += bonus # Acumula la bonificación

            print(
                f"[Robot Bonificado] Resolviendo {self.n} reinas en {execution_time:.2f} segundos. Bonificación total: {self.total_bonus}"
            )

class HumanoOptimizado:
    def __init__(self, env, n):
        self.env = env
        self.n = n
        self.execution_times = [] # Lista para almacenar los tiempos de ejecución
        env.process(self.run()) # Inicia el proceso de simulación

    def solve_n_queens(self, n, user_help=False):
        # Simula el tiempo que tarda en resolver el problema de las N-reinas
        base_time = random.uniform(n * 0.5, n * 0.8)
        # Ajustar tiempo de acuerdo al humano optimizado
        if user_help:
            base_time *= 0.5  # Reducir tiempo si hay ayuda
        return base_time # Retorna el tiempo ajustado

    def ask_for_help(self, n):
        # 70% de probabilidades de recibir ayuda
        return random.random() < 0.7

    def run(self):
         # Método que ejecuta el ciclo de resolución del problema
        while True:
            # Simula un tiempo entre intentos
            yield self.env.timeout(random.uniform(10, 20))
            start_time = self.env.now
            user_help = self.ask_for_help(self.n) # Pregunta si el usuario ayuda
            execution_time = self.solve_n_queens(self.n, user_help) # Simula el tiempo real
            yield self.env.timeout(execution_time)  # Simula el tiempo real
            self.execution_times.append(execution_time) # Almacena el tiempo de ejecución

            if user_help:
                print(f"[Ayuda] El usuario asistió en la resolución del problema de {self.n} reinas.")
            print(
                f"[Humano Optimizado] Resolviendo {self.n} reinas en {execution_time:.2f} segundos."
            )

def main(n):
    env = simpy.Environment()
    robot = RobotBonificado(env, n)
    humano = HumanoOptimizado(env, n)
    env.run(until=480)  # Simula 480 unidades de tiempo

if __name__ == "__main__":
    n = 8  # Valor de las n reinas
    main(n)