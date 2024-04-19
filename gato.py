import tkinter as tk
from tkinter import messagebox
import math

class Gato:
    def __init__(self):
        self.ventana=tk.Tk()
        self.ventana.title("Gato")
        self.jugador = "X"
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        self.botones = [[None for _ in range(3)] for _ in range(3)]

        for i in range (3):
            for j in range (3):
                self.botones[i][j] = tk.Button(self.ventana, text = " ", font = "consolas 30", width=10
                                                    , height=5, command = lambda fila = i, col = j: self.Seleccionar(fila, col))
                self.botones[i][j].grid(row=i, column=j)
    
    def movimientos_disponibles(self):
        movimientos = []
        for i in range(3):
            for j in range(3):
                if self.tablero[i][j] == ' ':
                    movimientos.append((i, j))
        return movimientos

    def evaluar_estado(self):
        # Verificar si alguien ganó
        for i in range(3):
            # Filas
            if self.tablero[i][0] == self.tablero[i][1] == self.tablero[i][2] != ' ':
                return 1 if self.tablero[i][0] == 'O' else -1
            # Columnas
            if self.tablero[0][i] == self.tablero[1][i] == self.tablero[2][i] != ' ':
                return 1 if self.tablero[0][i] == 'O' else -1
        # Diagonales
        if self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2] != ' ':
            return 1 if self.tablero[0][0] == 'O' else -1
        if self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0] != ' ':
            return 1 if self.tablero[0][2] == 'O' else -1
        # Si no hay ganador, verificar si hay empate
        if ' ' not in [casilla for fila in self.tablero for casilla in fila]:
            return 0  # Empate
        # Si el juego no ha terminado, devuelve None
        return None

    def minimax(self, profundidad, es_maximizando):
        resultado = self.evaluar_estado()
        
        # Si el juego ha terminado o la profundidad máxima ha sido alcanzada, retorna la evaluación del estado
        if resultado is not None:
            return resultado
        
        if es_maximizando:
            mejor_valor = -math.inf
            for movimiento in self.movimientos_disponibles():
                self.tablero[movimiento[0]][movimiento[1]] = 'O'
                valor = self.minimax(profundidad + 1, False)
                self.tablero[movimiento[0]][movimiento[1]] = ' '  # Deshacer el movimiento
                mejor_valor = max(mejor_valor, valor)
            return mejor_valor
        else:
            mejor_valor = math.inf
            for movimiento in self.movimientos_disponibles():
                self.tablero[movimiento[0]][movimiento[1]] = 'X'
                valor = self.minimax(profundidad + 1, True)
                self.tablero[movimiento[0]][movimiento[1]] = ' '  # Deshacer el movimiento
                mejor_valor = min(mejor_valor, valor)
            return mejor_valor
    
    def movimiento_optimo(self):
        mejor_movimiento = None
        mejor_valor = -math.inf
        for movimiento in self.movimientos_disponibles():
            self.tablero[movimiento[0]][movimiento[1]] = 'O'
            valor = self.minimax(0, False)
            self.tablero[movimiento[0]][movimiento[1]] = ' '  # Deshacer el movimiento
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = movimiento
        return mejor_movimiento
    
    def SeleccionarCompu(self):
        disponible = []
        disponible = self.movimientos_disponibles()
        if disponible:
            movimiento = self.movimiento_optimo()
            self.tablero[movimiento[0]][movimiento[1]] = self.jugador
            self.botones[movimiento[0]][movimiento[1]]["text"] = self.jugador
            self.botones[movimiento[0]][movimiento[1]]["state"] = "disabled"
            resultado = self.evaluar_estado()
            if resultado is not None:
                if resultado == 1:
                    messagebox.showinfo("Ganador", "Gana la computadora")
                elif resultado == 0:
                    messagebox.showinfo("Empate", "Empate")

    def Seleccionar(self, fila, col):
        if self.tablero[fila][col] == " ":
            self.tablero[fila][col] = self.jugador
            self.botones[fila][col]["text"] = self.jugador
            self.botones[fila][col]["state"] = "disabled"
        resultado = self.evaluar_estado()
        if resultado is not None:
            if resultado == -1:
                messagebox.showinfo("Ganador", f"El jugador {self.jugador} gana")
            elif resultado == 0:
                messagebox.showinfo("Empate", "Empate")
        else:
            self.cambiarJugador()
            self.SeleccionarCompu()
            self.cambiarJugador()
    
    def cambiarJugador(self):
        if self.jugador == "X":
            self.jugador = "O"
        else:
            self.jugador = "X"

    def run(self):
        self.ventana.mainloop()
        
if __name__ == "__main__":
    juego = Gato()
    juego.run()