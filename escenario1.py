import simulacion
import simpy
import random
import time

class RobotOptimizado(simulacion.Robot):
    def run(self):
        """
        Método principal del robot optimizado, que simula su actividad en la simulación.
        Penaliza los tiempos de llegada y resuelve tableros con tiempos más largos
        dependiendo del tamaño del tablero.
        """
        while True:
            # Simula un tiempo de espera entre 10 y 30 unidades antes de que el robot actúe
            yield self.env.timeout(random.uniform(10, 30))  # Penalizar tiempos de llegada
            
            # Simula el tiempo de ejecución para resolver el problema de las N reinas
            # Este tiempo depende del tamaño del tablero (n), siendo más lento para tableros grandes
            simulated_time = random.uniform(self.n * 1, self.n * 2)  # Más lento para tableros grandes
            
            self.execution_times.append(simulated_time)
            print(f"[RobotOptimizado] Resolviendo {self.n} reinas en {simulated_time:.2f} segundos.")

class HumanoOptimizado(simulacion.Humano):
    def solve_n_queens(self, n):
        """
        Método personalizado para resolver el problema de las N reinas utilizando un algoritmo recursivo.
        Coloca las reinas en el tablero llamando al método recursivo place_queen.
        """
        # Inicializa el tablero con -1, indicando que no hay reinas colocadas
        board = [-1] * n
        # Llama al método recursivo para colocar las reinas
        self.place_queen(board, 0)
        # Retorna el tablero con las posiciones finales de las reinas
        return board

def main(n):
    """
    Configura y ejecuta la simulación utilizando SimPy.
    Crea instancias de RobotOptimizado y HumanoOptimizado y las simula durante 480 unidades de tiempo.
    """
    # Crea un entorno de simulación de SimPy
    env = simpy.Environment()
    # Instancia un robot optimizado para el tamaño del tablero dado (n)
    robot = RobotOptimizado(env, n)
    # Instancia un humano optimizado para el tamaño del tablero dado (n)
    humano = HumanoOptimizado(env, n)
    # Ejecuta la simulación hasta que se agoten los 480 minutos
    env.run(until=480)

if __name__ == "__main__":
    # Tamaño predeterminado del tablero (n)
    n = 8  
    main(n)