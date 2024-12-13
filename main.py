import tkinter as tk
import interfaz

def main():
    """
    Función principal que inicializa la ventana de la aplicación.
    - Crea una instancia de la ventana principal utilizando `Tk`.
    - Crea una instancia de la clase `Interfaz` para manejar los elementos y eventos de la ventana.
    - Ejecuta el bucle principal para mantener la ventana abierta y responder a las interacciones del usuario.
    """
    root = tk.Tk()
    app = interfaz.Interfaz(root)
    root.mainloop()

if __name__ == "__main__":
    main()