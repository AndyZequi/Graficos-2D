import pygame
import math
import numpy as np

# Configuración inicial de Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Función para rotar un polígono en torno a su centro
def rotate_polygon(points, angle, center):
    angle = math.radians(angle)
    rot_matrix = np.array([[math.cos(angle), -math.sin(angle)], 
                           [math.sin(angle), math.cos(angle)]])
    return [(int(center[0] + (x - center[0]) * rot_matrix[0][0] + (y - center[1]) * rot_matrix[0][1]),
             int(center[1] + (x - center[0]) * rot_matrix[1][0] + (y - center[1]) * rot_matrix[1][1])) 
            for x, y in points]

# Definir un rectángulo inicial (como polígono)
polygon = [(300, 200), (400, 200), (400, 300), (300, 300)]
polygon_center = (350, 250)
angle = 80  # Ángulo de rotación

# Función para obtener AABB de un polígono
def get_AABB(points):
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)
    return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)

running = True
while running:
    screen.fill((30, 30, 30))  # Fondo oscuro

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotar polígono
    rotated_polygon = rotate_polygon(polygon, angle, polygon_center)

    # Calcular AABB
    aabb = get_AABB(rotated_polygon)

    # Dibujar polígono real
    pygame.draw.polygon(screen, (0, 255, 0), rotated_polygon, 2)

    # Dibujar AABB en rojo
    pygame.draw.rect(screen, (255, 0, 0), aabb, 2)

    # Incrementar ángulo de rotación
    angle += 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
