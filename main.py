import tkinter as  tk
ventana = tk.Tk()
ventana.title("Tablero de ajedrez")

Dimension = 8
Tamaño_casilla = 80
Ancho = Alto = Dimension * Tamaño_casilla

color_Blanco = (255, 255, 255)
color_Negro = (0, 0, 0)

lienzo = tk.Canvas(ventana, width = 8 * Tamaño_casilla, height= 8 * Tamaño_casilla)
lienzo.pack()

for fila in  range(8):
    for columna in range(8):

        x1 = columna * Tamaño_casilla
        y1 = fila * Tamaño_casilla
        x2 = columna * Tamaño_casilla
        y2 = fila * Tamaño_casilla


        if (fila + columna) % 2 == 0:
            color = color_Blanco
        else:
            color = color_Negro

        lienzo.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

ventana.mainloop()

