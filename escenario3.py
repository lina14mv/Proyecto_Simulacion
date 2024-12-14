import simulacion
import simpy
import random
import time

class InteraccionRobot(simulacion.Robot):
    def run(self):
        """
        Método que simula el comportamiento del robot en la simulación.
        Cada cierto tiempo, intenta resolver el problema de las N reinas.
        """
        while True:
            # Simula un tiempo de espera aleatorio entre 10 y 30 unidades de tiempo
            yield self.env.timeout(random.uniform(10, 30))
            # Simula el tiempo de resolución del problema
            simulated_time = random.uniform(self.n * 0.05, self.n * 0.2)
            # Registra el tiempo de ejecución
            self.execution_times.append(simulated_time)
            print(f"[InteraccionRobot] Resolviendo {self.n} reinas en {simulated_time:.2f} segundos.")

    def ask_for_help(self, n):
        """
        Simula si el robot solicita ayuda del usuario.
        Retorna True con alta probabilidad, pero ocasionalmente puede retornar False.
        """
        return random.choice([True, True, False])

    def solve_n_queens(self, n, method='las_vegas', user_help=False):
        """
        Resuelve el problema de las N reinas utilizando un método aleatorio (Las Vegas).
        Permite la opción de asistencia del usuario para facilitar la resolución.
        """
        solutions = [] # Lista para almacenar soluciones encontradas
        attempts = 0 # Contador de intentos
        # Realiza intentos hasta encontrar una solución o alcanzar el límite de intentos
        while not solutions and attempts < 100:
            # Genera un tablero inicial aleatorio
            board = self.generate_random_board(n)
            # Verifica si el tablero generado es una solución válida
            if self.backtrack(board, 0):
                solutions.append(board)
            attempts += 1 # Incrementa el número de intentos

            # Si el usuario ayuda, imprime un mensaje
            if user_help:
                print(f"[Ayuda] El usuario asistió en la resolución del problema de {n} reinas.")
        return solutions

class InteraccionHumano(simulacion.Humano):
    def run(self):
        """
        Método que simula el comportamiento del humano en la simulación.
        Intenta resolver el problema de las N reinas, con o sin ayuda.
        """
        while True:
            # Simula un tiempo de espera aleatorio entre 10 y 30 unidades de tiempo
            yield self.env.timeout(random.uniform(10, 30))
            # Inicia el cronómetro para medir el tiempo de resolución
            start_time = time.time()
            # Determina si el humano recibe ayuda
            user_help = self.ask_for_help(self.n)
            # Resuelve el problema de las N reinas
            self.solve_n_queens(self.n, user_help=user_help)
            # Calcula el tiempo total de resolución
            self.execution_time = time.time() - start_time
            # Registra el tiempo de ejecución
            self.execution_times.append(self.execution_time)
            print(f"[Interacción Humano] Resolviendo {self.n} reinas en {self.execution_time:.2f} segundos.")

    def ask_for_help(self, n):
        """
        Simula si el humano solicita ayuda.
        Retorna True o False de manera equitativa.
        """
        return random.choice([True, False])

    def solve_n_queens(self, n, user_help=False):
        """
        Resuelve el problema de las N reinas, simulando tiempos humanos.
        Puede reducir el tiempo si se recibe ayuda.
        """
        # Simula el tiempo necesario para resolver el problema
        simulated_time = random.uniform(n * 0.8, n * 1.2)  # Simula tiempo humano
        # Introduce una pausa para simular el tiempo humano sin causar largas esperas
        time.sleep(simulated_time / 10)  # Divide el tiempo para evitar largas pausas
        # Reduce el tiempo de simulación si hay ayuda del usuario
        if user_help:
            simulated_time *= 0.2  # Reducir tiempo si hay ayuda
            print(f"[Ayuda] El usuario asistió en la resolución del problema de {n} reinas.")
        # Retorna un tablero vacío como resultado simulado
        return [-1] * n  # Simula un tablero vacío como resultado

def main(n):
    """
    Configura el entorno de simulación y ejecuta las interacciones
    entre el robot y el humano durante 28800 unidades de tiempo.
    """
    env = simpy.Environment()
    robot = InteraccionRobot(env, n)
    humano = InteraccionHumano(env, n)
    env.run(until=28800)

if __name__ == "__main__":
    n = 8
    main(n)