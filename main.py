import pygame, sys

pygame.init()

Dimension = 8
Tamaño_casilla = 80
Ancho = Alto = Dimension * Tamaño_casilla

pantalla = pygame.display.set_mode((Ancho, Alto))
pygame.display.set_caption("Tablero de ajedrez")

fuente = pygame.font.SysFont("arial", 60)

BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

tablero_inicial = [
["t", "c", "a", "d", "r", "a", "c", "t"],
["p", "p", "p", "p", "p", "p", "p","p"],
["", "", "", "", "", "", "", ""],
["", "", "", "", "", "", "", ""],
["", "", "", "", "", "", "", ""],
["", "", "", "", "", "", "", ""],
["P", "P", "P", "P", "P", "P", "P", "P"],
["T", "C", "A", "D", "R", "A", "C", "T"],
]
dibujo_piezas= {
  "t": "♜", "c": "♞", "a": "♝", "d": "♛", "r": "♚", "p": "♟",

    "T": "♖", "C": "♘", "A": "♗", "D": "♕", "R": "♔", "P": "♙"
}

jugando = True
while jugando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.quit()

    for fila in  range(8):
       for columna in range(8):

            x1 = columna * Tamaño_casilla
            y1 = fila * Tamaño_casilla
            

            if (fila + columna) % 2 == 0:
                color = BLANCO
            else:
                color = NEGRO

            pygame.draw.rect(pantalla, color, [x1, y1, Tamaño_casilla, Tamaño_casilla])
            
            letra = tablero_inicial[fila][columna]

            if letra != "":
                simbolo_real = dibujo_piezas[letra]

                if letra in ["T", "C", "A","D", "R", "P"]:
                    color_ficha = BLANCO

                else:
                    color_ficha = GRIS

                texto_imagen = fuente.render(simbolo_real, True, color_ficha)

                centro_x = x1 + 15
                centro_y = y1 + 5

                pantalla.blit(texto_imagen, ( centro_x, centro_y))
    pygame.display.flip()