import pygame
import sys
import time


ANCHO = 640
ALTO = 760  
TAM_CASILLA = ANCHO // 8
COLORES = [(240, 217, 181), (181, 136, 99)]  
COLOR_TEXTO = (255, 255, 255)
COLOR_RELOJ = (40, 40, 40)
COLOR_SELECCION = (100, 200, 100, 120)  
FICHAS = {
    'r': ('♜', 'Torre Negra'),
    'n': ('♞', 'Caballo Negro'),
    'b': ('♝', 'Alfil Negro'),
    'q': ('♛', 'Reina Negra'),
    'k': ('♚', 'Rey Negro'),
    'p': ('♟', 'Peón Negro'),
    'R': ('♖', 'Torre Blanca'),
    'N': ('♘', 'Caballo Blanco'),
    'B': ('♗', 'Alfil Blanco'),
    'Q': ('♕', 'Reina Blanca'),
    'K': ('♔', 'Rey Blanco'),
    'P': ('♙', 'Peón Blanco')
}


TABLERO_INICIAL = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
]

# ------------------- INICIALIZACIÓN -------------------
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ajedrez Completo")
fuente_fichas = pygame.font.SysFont('segoeuisymbol', 48)
fuente_info = pygame.font.SysFont('Arial', 24)
fuente_reloj = pygame.font.SysFont('Arial', 36)


tablero = [fila.copy() for fila in TABLERO_INICIAL]
ficha_seleccionada = None 
nombre_ficha_mostrado = ""
ultimo_tiempo = time.time()
tiempo_blanco = 600  
tiempo_negro = 600
turno_blanco = True  


def dibujar_tablero():
    """Dibuja las casillas del tablero"""
    for fila in range(8):
        for col in range(8):
            color = COLORES[(fila + col) % 2]
            pygame.draw.rect(pantalla, color, 
                             (col * TAM_CASILLA, fila * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA))
    
   
    if ficha_seleccionada:
        fila_sel, col_sel = ficha_seleccionada
        resaltado = pygame.Surface((TAM_CASILLA, TAM_CASILLA), pygame.SRCALPHA)
        resaltado.fill(COLOR_SELECCION)
        pantalla.blit(resaltado, (col_sel * TAM_CASILLA, fila_sel * TAM_CASILLA))

def dibujar_fichas():
    """Dibuja las fichas con sus símbolos"""
    for fila in range(8):
        for col in range(8):
            pieza = tablero[fila][col]
            if pieza:
                simbolo, _ = FICHAS[pieza]
                
                color_texto = (255, 255, 255) if pieza.isupper() else (0, 0, 0)
                texto = fuente_fichas.render(simbolo, True, color_texto)
                rect = texto.get_rect(center=(col * TAM_CASILLA + TAM_CASILLA//2,
                                              fila * TAM_CASILLA + TAM_CASILLA//2))
                pantalla.blit(texto, rect)

def dibujar_inferior():
    """Dibuja la zona inferior con nombre de ficha y relojes"""
    
    pygame.draw.rect(pantalla, COLOR_RELOJ, (0, ANCHO, ANCHO, ALTO - ANCHO))
    
    
    texto_info = fuente_info.render(f"Ficha: {nombre_ficha_mostrado}", True, COLOR_TEXTO)
    pantalla.blit(texto_info, (20, ANCHO + 10))
    
   
    def formato_tiempo(segundos):
        if segundos < 0:
            return "00:00"
        m = int(segundos // 60)
        s = int(segundos % 60)
        return f"{m:02d}:{s:02d}"
    
    color_blanco = (255, 255, 0) if turno_blanco else COLOR_TEXTO
    color_negro = (255, 255, 0) if not turno_blanco else COLOR_TEXTO
    
    texto_blanco = fuente_reloj.render(f"Blancas: {formato_tiempo(tiempo_blanco)}", True, color_blanco)
    texto_negro = fuente_reloj.render(f"Negras: {formato_tiempo(tiempo_negro)}", True, color_negro)
    
    pantalla.blit(texto_blanco, (20, ANCHO + 50))
    pantalla.blit(texto_negro, (320, ANCHO + 50))

def es_movimiento_valido(origen, destino, pieza):
    """Verifica si un movimiento cumple con las reglas básicas del ajedrez"""
    fila_orig, col_orig = origen
    fila_dest, col_dest = destino
    
    
    if origen == destino:
        return False
    
    
    pieza_destino = tablero[fila_dest][col_dest]
    if pieza_destino and pieza.isupper() == pieza_destino.isupper():
        return False

    
    if pieza.lower() == 'p':  
        direccion = -1 if pieza.isupper() else 1
        avance = fila_dest - fila_orig
        

        if col_dest == col_orig:
            if avance == direccion and not pieza_destino:
                return True
            if avance == 2 * direccion and fila_orig in (1, 6) and not pieza_destino and not tablero[fila_orig + direccion][col_orig]:
                return True
        
        elif abs(col_dest - col_orig) == 1 and avance == direccion and pieza_destino:
            return True

    elif pieza.lower() == 'r': 
        if fila_orig == fila_dest or col_orig == col_dest:
            return camino_libre(origen, destino)

    elif pieza.lower() == 'n':  
        return (abs(fila_dest - fila_orig) == 2 and abs(col_dest - col_orig) == 1) or \
               (abs(fila_dest - fila_orig) == 1 and abs(col_dest - col_orig) == 2)

    elif pieza.lower() == 'b':  
        if abs(fila_dest - fila_orig) == abs(col_dest - col_orig):
            return camino_libre(origen, destino)

    elif pieza.lower() == 'q':  
        if fila_orig == fila_dest or col_orig == col_dest or abs(fila_dest - fila_orig) == abs(col_dest - col_orig):
            return camino_libre(origen, destino)

    elif pieza.lower() == 'k': 
        return max(abs(fila_dest - fila_orig), abs(col_dest - col_orig)) == 1

    return False

def camino_libre(origen, destino):
    """Verifica que no haya piezas en medio del camino"""
    fila_orig, col_orig = origen
    fila_dest, col_dest = destino

    paso_fila = 0 if fila_orig == fila_dest else (1 if fila_dest > fila_orig else -1)
    paso_col = 0 if col_orig == col_dest else (1 if col_dest > col_orig else -1)

    fila_actual = fila_orig + paso_fila
    col_actual = col_orig + paso_col

    while fila_actual != fila_dest or col_actual != col_dest:
        if tablero[fila_actual][col_actual] != '':
            return False
        fila_actual += paso_fila
        col_actual += paso_col
    return True

def manejar_click(pos):
    """Detecta clic, selecciona o mueve la ficha"""
    global ficha_seleccionada, nombre_ficha_mostrado, turno_blanco

    x, y = pos
    if y >= ANCHO: 
        return

    col = x // TAM_CASILLA
    fila = y // TAM_CASILLA
    pieza_actual = tablero[fila][col]

    
    if not ficha_seleccionada:
        if pieza_actual:
            
            if (turno_blanco and pieza_actual.isupper()) or (not turno_blanco and pieza_actual.islower()):
                ficha_seleccionada = (fila, col)
                _, nombre_ficha_mostrado = FICHAS[pieza_actual]
        return
    
    fila_orig, col_orig = ficha_seleccionada
    pieza = tablero[fila_orig][col_orig]

    if es_movimiento_valido((fila_orig, col_orig), (fila, col), pieza):
        
        tablero[fila][col] = pieza
        tablero[fila_orig][col_orig] = ''
        turno_blanco = not turno_blanco  
        nombre_ficha_mostrado = "Movimiento realizado"
    else:
        nombre_ficha_mostrado = "Movimiento no válido"


    ficha_seleccionada = None


reloj = pygame.time.Clock()
ejecutando = True

while ejecutando:
    tiempo_actual = time.time()
    delta = tiempo_actual - ultimo_tiempo
    ultimo_tiempo = tiempo_actual

    
    if turno_blanco and tiempo_blanco > 0:
        tiempo_blanco -= delta
    elif not turno_blanco and tiempo_negro > 0:
        tiempo_negro -= delta

    
    if tiempo_blanco <= 0 or tiempo_negro <= 0:
        nombre_ficha_mostrado = "¡Se acabó el tiempo!"

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.MOUSEBUTTONDOWN and (tiempo_blanco > 0 and tiempo_negro > 0):
            manejar_click(evento.pos)

    
    pantalla.fill((0, 0, 0))
    dibujar_tablero()
    dibujar_fichas()
    dibujar_inferior()

    pygame.display.flip()
    reloj.tick(30)

pygame.quit()
sys.exit()