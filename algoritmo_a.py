import matplotlib.pyplot as plt
import numpy as np
import heapq

# Colores
WHITE = 1
BLACK = 0
GREEN = 2
RED = 3
YELLOW = 4

# Mapa de 20x15
WIDTH = 20
HEIGHT = 15

# Celdas de inicio y fin
START = (7, 6)
END = (14, 5)

# Funciones de A* y visualización

def heuristica(a, b):
    """Heurística de Manhattan"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(start, end, grid):
    """Algoritmo A*"""
    open_list = []
    closed_list = set()
    came_from = {}

    # Celdas de inicio
    g_score = {start: 0}
    f_score = {start: heuristica(start, end)}

    # Poner el punto inicial en la lista abierta
    heapq.heappush(open_list, (f_score[start], start))

    while open_list:
        _, current = heapq.heappop(open_list)

        # Si llegamos al final, reconstruir el camino
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Devuelve el camino invertido

        closed_list.add(current)

        # Revisamos las celdas vecinas
        neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # 4 direcciones
        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)

            # Verifica si la vecina está dentro de los límites y no es un obstáculo
            if 0 <= neighbor[0] < WIDTH and 0 <= neighbor[1] < HEIGHT and grid[neighbor[1]][neighbor[0]] != 1:
                if neighbor in closed_list:
                    continue

                tentative_g_score = g_score.get(current, float('inf')) + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristica(neighbor, end)

                    if neighbor not in [i[1] for i in open_list]:
                        heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None  # Si no hay camino

def draw_grid(grid, path=None):
    """Dibuja el mapa"""
    grid_display = np.ones((HEIGHT, WIDTH)) * WHITE  # Inicializa el mapa con celdas blancas

    # Obstáculos
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if grid[y][x] == 1:
                grid_display[y][x] = BLACK

    # Dibuja el camino
    if path:
        for p in path:
            grid_display[p[1]][p[0]] = YELLOW

    # Dibuja el inicio y el final
    grid_display[START[1]][START[0]] = GREEN
    grid_display[END[1]][END[0]] = RED

    plt.imshow(grid_display, cmap="tab20b", interpolation='nearest')
    plt.axis('off')  # Oculta los ejes
    plt.show()

def main():
    # Crear un mapa con obstáculos
    grid = np.zeros((HEIGHT, WIDTH))  # 0 = libre, 1 = obstáculo

    # Bloques de obstáculos
    obstacles = [
        (5, 6), (5, 7), (5, 8), (5, 9),
        (6, 9), (7, 9), (8, 9), (9, 9), (11, 3), (10, 9),
        (10, 8), (10, 7), (10, 6), (10, 5), (10, 4),
        (9, 4), (8, 4), (7, 4), (6, 4),
        (12, 3), (13, 3), (14, 3), (15, 3), (16, 3),
        (16, 4), (16, 5), (16, 6), (16, 7), (16, 8),
        (15, 8), (14, 8), (13, 8), (12, 8)
    ]

    # Coloca los obstáculos en la cuadrícula
    for x, y in obstacles:
        grid[y][x] = 1

    # Ejecutar A*
    path = a_star(START, END, grid)
    
    # Dibujar el resultado
    draw_grid(grid, path)

if __name__ == "__main__":
    main()