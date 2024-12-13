import tkinter as tk
from tkinter import messagebox
from simulacion import ejecutar_simulacion
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

class Interfaz:
    def __init__(self, master):
        """
        Constructor de la clase Interfaz. Inicializa los componentes de la ventana.
        :param master: Ventana principal de Tkinter.
        """
        self.master = master
        master.title("Simulación N Reinas")

        # Etiqueta y campo para ingresar el tamaño del tablero
        self.label = tk.Label(master, text="Ingrese el tamaño del tablero (4, 5, 6, 8, 10, 12 o 15):")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        # Etiqueta y campo para seleccionar el escenario
        self.label_escenario = tk.Label(master, text="Seleccione el escenario (1, 2 o 3):")
        self.label_escenario.pack()

        self.entry_escenario = tk.Entry(master)
        self.entry_escenario.pack()

        # Botón para iniciar la simulación
        self.boton = tk.Button(master, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.boton.pack()

        # Variables para almacenar resultados y ganancias
        self.resultados = [] # Lista para guardar los resultados de cada simulación
        self.ganancia = 0 # Ganancia total acumulada

    def iniciar_simulacion(self):
        """
        Inicia la simulación basada en los valores ingresados por el usuario.
        """
        try:
            n = int(self.entry.get())
            if n not in [4, 5, 6, 8, 10, 12, 15]:
                raise ValueError("Tamaño del tablero no válido")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        try:
            escenario = int(self.entry_escenario.get())
            if escenario not in [1, 2, 3]:
                raise ValueError("Escenario no válido")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        print(f"Se iniciará la simulación con n = {n} y escenario = {escenario}")

        # Ejecutar la simulación y capturar tiempos de robot y humano
        robot_times, humano_times = ejecutar_simulacion(n, escenario)
        for robot_time, humano_time in zip(robot_times, humano_times):
            ganador = "Humano" if humano_time < robot_time else "Robot"
            self.resultados.append((n, robot_time, humano_time, ganador))
            
            # Actualizar ganancia dependiendo del ganador
            if ganador == "Humano":
                self.ganancia += 15
            else:
                self.ganancia -= 10
            print(f"Robot: {robot_time:.2f} segundos, Humano: {humano_time:.2f} segundos, Ganador: {ganador}")

        print(f"Ganancia total: {self.ganancia}")
        self.generar_grafica() # Generar gráfica al finalizar la simulación

    def generar_grafica(self):
        """
        Genera gráficas basadas en los resultados de las simulaciones:
        1. Tiempos de ejecución promedio.
        2. Número de victorias por tamaño de tablero.
        """
        # Agrupar resultados por tamaño del tablero
        resultados_por_tamano = defaultdict(lambda: {'robot_times': [], 'humano_times': [], 'ganadores': []})
        for resultado in self.resultados:
            n, robot_time, humano_time, ganador = resultado
            resultados_por_tamano[n]['robot_times'].append(robot_time)
            resultados_por_tamano[n]['humano_times'].append(humano_time)
            resultados_por_tamano[n]['ganadores'].append(ganador)

        # Calcular tiempos promedio y número de victorias por tamaño del tablero
        tamano_tablero = sorted(resultados_por_tamano.keys())
        robot_promedios = []
        humano_promedios = []
        robot_victorias = []
        humano_victorias = []

        for n in tamano_tablero:
            robot_promedios.append(np.mean(resultados_por_tamano[n]['robot_times']))
            humano_promedios.append(np.mean(resultados_por_tamano[n]['humano_times']))
            robot_victorias.append(resultados_por_tamano[n]['ganadores'].count('Robot'))
            humano_victorias.append(resultados_por_tamano[n]['ganadores'].count('Humano'))

        # Configuración de las barros en las gráficas
        bar_width = 0.35
        index = np.arange(len(tamano_tablero))

        # Gráfica de tiempos de ejecución promedio
        plt.figure(figsize=(10, 5))
        plt.bar(index, robot_promedios, bar_width, label='Robot', color='blue')
        plt.bar(index + bar_width, humano_promedios, bar_width, label='Humano', color='red')
        plt.xlabel('Tamaño del Tablero (n)')
        plt.ylabel('Tiempo de Ejecución Promedio (segundos)')
        plt.title('Comparación de Tiempos de Ejecución Promedio: Robot vs Humano')
        plt.xticks(index + bar_width / 2, tamano_tablero)
        plt.legend()
        plt.grid(True)
        plt.savefig('tiempos_ejecucion_promedio.png')  # Guardar la gráfica como archivo PNG
        plt.show()

        # Gráfica de número de victorias
        plt.figure(figsize=(10, 5))
        plt.bar(index, robot_victorias, bar_width, label='Robot', color='blue')
        plt.bar(index + bar_width, humano_victorias, bar_width, label='Humano', color='red')
        plt.xlabel('Tamaño del Tablero (n)')
        plt.ylabel('Número de Victorias')
        plt.title('Comparación de Victorias: Robot vs Humano')
        plt.xticks(index + bar_width / 2, tamano_tablero)
        plt.legend()
        plt.grid(True)
        plt.savefig('victorias.png')  # Guardar la gráfica como archivo PNG
        plt.show()

def main():
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()

if __name__ == "__main__":
    main()