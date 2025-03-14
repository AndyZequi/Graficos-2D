import pygame
import noise
import numpy as np
import heapq  
import random  # Importar la librería para posiciones aleatorias

# Configuración del mapa
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 10
MAP_WIDTH = WIDTH // TILE_SIZE
MAP_HEIGHT = HEIGHT // TILE_SIZE

# Colores
WATER = (0, 0, 255)
GRASS = (0, 255, 0)
MOUNTAIN = (139, 69, 19)
PLAYER_COLOR = (255, 0, 0)
ENEMY_COLOR = (255, 255, 0)

# Generar el mapa con Perlin Noise
def generate_map(scale=20.0):
    world = np.zeros((MAP_WIDTH, MAP_HEIGHT))
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            nx, ny = x / scale, y / scale
            value = noise.pnoise2(nx, ny, octaves=6, persistence=0.5, lacunarity=2.0)
            world[x][y] = value
    return world

# Algoritmo A* para encontrar el mejor camino
def a_star(start, goal, map_data):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  

        neighbors = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in neighbors:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < MAP_WIDTH and 0 <= neighbor[1] < MAP_HEIGHT:
                if map_data[neighbor[0]][neighbor[1]] < -0.1:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

# Clase del Jugador
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
            if map_data[new_x][new_y] >= -0.1:
                self.x = new_x
                self.y = new_y

    def draw(self, screen):
        pygame.draw.rect(screen, PLAYER_COLOR, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Clase del Enemigo
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = []

    def update(self, player_pos):
        if not self.path or (self.x, self.y) == self.path[-1]:
            self.path = a_star((self.x, self.y), player_pos, map_data)

        if self.path:
            self.x, self.y = self.path.pop(0)

    def draw(self, screen):
        pygame.draw.rect(screen, ENEMY_COLOR, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Supervivencia - Game Over")

# Generar el mapa y las entidades
map_data = generate_map()
player = Player(MAP_WIDTH // 2, MAP_HEIGHT // 2)

# Crear múltiples enemigos en posiciones aleatorias
num_enemies = 5  # Cambia este número para más enemigos
enemies = []

for _ in range(num_enemies):
    while True:
        ex, ey = random.randint(0, MAP_WIDTH - 1), random.randint(0, MAP_HEIGHT - 1)
        if map_data[ex][ey] >= -0.1 and (ex, ey) != (player.x, player.y):
            enemies.append(Enemy(ex, ey))
            break

# Fuente para el mensaje de Game Over
font = pygame.font.Font(None, 50)

# Función para dibujar el mapa
def draw_map():
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            value = map_data[x][y]
            if value < -0.1:
                color = WATER
            elif value < 0.2:
                color = GRASS
            else:
                color = MOUNTAIN
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Bucle principal del juego
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))
    draw_map()
    player.draw(screen)
    
    # Dibujar y actualizar todos los enemigos
    for enemy in enemies:
        enemy.draw(screen)
        enemy.update((player.x, player.y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimiento del jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move(0, -1)
    if keys[pygame.K_DOWN]:
        player.move(0, 1)
    if keys[pygame.K_LEFT]:
        player.move(-1, 0)
    if keys[pygame.K_RIGHT]:
        player.move(1, 0)

    # Verificar colisión con cualquier enemigo (Game Over)
    for enemy in enemies:
        if (player.x, player.y) == (enemy.x, enemy.y):
            text = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)  # Esperar 2 segundos antes de salir
            running = False
            break  # Salir del loop de enemigos

    pygame.display.flip()
    clock.tick(10)  

pygame.quit()
