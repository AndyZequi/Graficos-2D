import heapq
import pygame

# Definir colores
GRIS = (169, 169, 169)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
NEGRO = (0, 0, 0)

# Dimensiones del grid
FILAS = 10
COLUMNAS = 10
TAMANO_CELDA = 50

# Inicializar mapa con obstáculos (1 = obstáculo, 0 = camino libre)
mapa = [
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 1]
]

# Posición de inicio y meta
inicio = (1, 0)
meta = (9, 8)

# Direcciones posibles (arriba, abajo, izquierda, derecha)
DIRECCIONES = [(0, 1), (0, -1), (1, 0), (-1, 0)]


# Clase para nodos del A*
class Nodo:
    def __init__(self, x, y, costo, heuristica, padre=None):
        self.x = x
        self.y = y
        self.costo = costo
        self.heuristica = heuristica
        self.padre = padre

    def __lt__(self, otro):
        return (self.costo + self.heuristica) < (otro.costo + otro.heuristica)


# Función heurística Manhattan
def heuristica_manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


# Algoritmo A*
def a_estrella(inicio, fin):
    abiertos = []
    visitados = set()
    nodo_inicio = Nodo(inicio[0], inicio[1], 0, heuristica_manhattan(*inicio, *fin))
    heapq.heappush(abiertos, nodo_inicio)

    while abiertos:
        actual = heapq.heappop(abiertos)

        if (actual.x, actual.y) in visitados:
            continue
        visitados.add((actual.x, actual.y))

        if (actual.x, actual.y) == fin:
            camino = []
            while actual:
                camino.append((actual.x, actual.y))
                actual = actual.padre
            return camino[::-1]  # Retorna el camino en orden correcto

        for dx, dy in DIRECCIONES:
            nx, ny = actual.x + dx, actual.y + dy
            if 0 <= nx < FILAS and 0 <= ny < COLUMNAS and mapa[nx][ny] == 0:
                if (nx, ny) not in visitados:
                    nuevo_nodo = Nodo(nx, ny, actual.costo + 1, heuristica_manhattan(nx, ny, *fin), actual)
                    heapq.heappush(abiertos, nuevo_nodo)

    return None  # No hay camino


# Inicializar Pygame
pygame.init()
pantalla = pygame.display.set_mode((COLUMNAS * TAMANO_CELDA, FILAS * TAMANO_CELDA))
pygame.display.set_caption("Algoritmo A* - Búsqueda de Caminos")

# Ejecutar algoritmo A*
camino = a_estrella(inicio, meta)

# Dibujar el grid
def dibujar_grid():
    pantalla.fill(NEGRO)
    for fila in range(FILAS):
        for col in range(COLUMNAS):
            color = GRIS if mapa[fila][col] == 0 else AZUL
            pygame.draw.rect(pantalla, color, (col * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
            pygame.draw.rect(pantalla, NEGRO, (col * TAMANO_CELDA, fila * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA), 1)

    # Dibujar inicio y meta
    pygame.draw.rect(pantalla, ROJO, (inicio[1] * TAMANO_CELDA, inicio[0] * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))
    pygame.draw.rect(pantalla, VERDE, (meta[1] * TAMANO_CELDA, meta[0] * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))

    # Dibujar el camino en amarillo
    if camino:
        for (x, y) in camino:
            pygame.draw.rect(pantalla, AMARILLO, (y * TAMANO_CELDA, x * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))


# Bucle principal de Pygame
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    dibujar_grid()
    pygame.display.flip()

pygame.quit()