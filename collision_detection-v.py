import pygame
import numpy as np

# Configuración de Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# --- Algoritmo AABB (Bounding Box) ---
class AABB:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height

    def update_from_polygon(self, polygon):
        """Actualiza la AABB basándose en el polígono (solo funciona si está alineado)."""
        x_coords, y_coords = zip(*polygon.vertices)
        self.x, self.y = min(x_coords), min(y_coords)
        self.width, self.height = max(x_coords) - self.x, max(y_coords) - self.y

    def intersects(self, other):
        """Verifica si dos AABB se superponen."""
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

    def draw(self, color):
        """Dibuja el AABB en pantalla."""
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height), 2)

# --- Algoritmo SAT (Separating Axis Theorem) ---
class Polygon:
    def __init__(self, center, vertices):
        self.center = np.array(center)
        self.vertices = np.array(vertices)
        self.rotation = 0  # Ángulo de rotación en grados

    def move(self, dx, dy):
        """Mueve el polígono."""
        self.center += np.array([dx, dy])
        self.vertices += np.array([dx, dy])

    def rotate(self, angle):
        """Rota el polígono en sentido antihorario."""
        self.rotation += angle  # Guardamos el ángulo de rotación total
        rad = np.radians(angle)
        cos_a, sin_a = np.cos(rad), np.sin(rad)

        new_vertices = []
        for v in self.vertices:
            rotated = self.center + np.dot([[cos_a, -sin_a], [sin_a, cos_a]], (v - self.center))
            new_vertices.append(rotated)

        self.vertices = np.array(new_vertices)

    def get_axes(self):
        """Obtiene los ejes perpendiculares de cada lado del polígono."""
        axes = []
        for i in range(len(self.vertices)):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % len(self.vertices)]
            edge = p2 - p1
            normal = np.array([-edge[1], edge[0]])  # Perpendicular
            axes.append(normal / np.linalg.norm(normal))  # Normalizar
        return axes

    def project(self, axis):
        """Proyecta los vértices sobre un eje."""
        dots = np.dot(self.vertices, axis)
        return min(dots), max(dots)

    def check_collision(self, other):
        """Verifica colisión con otro polígono usando SAT."""
        for axis in self.get_axes() + other.get_axes():
            minA, maxA = self.project(axis)
            minB, maxB = other.project(axis)
            if maxA < minB or maxB < minA:
                return False  # No hay colisión
        return True  # Hay colisión

    def draw(self, color):
        """Dibuja el polígono en pantalla."""
        pygame.draw.polygon(screen, color, self.vertices, 2)

# --- Configuración de objetos ---
poly1 = Polygon([275, 200], [[225, 150], [325, 150], [350, 250], [250, 250]])
poly2 = Polygon([475, 350], [[425, 300], [525, 300], [550, 400], [450, 400]])

box1 = AABB(0, 0, 0, 0)  # Se actualizará con el polígono
box2 = AABB(0, 0, 0, 0)  # Se actualizará con el polígono

box1.update_from_polygon(poly1)
box2.update_from_polygon(poly2)

# Método de colisión actual ("AABB" o "SAT")
collision_method = "AABB"

# --- Loop principal ---
running = True
while running:
    screen.fill((30, 30, 30))

    # --- Manejo de eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:  # Cambiar método de colisión con TAB
                collision_method = "SAT" if collision_method == "AABB" else "AABB"
            if event.key == pygame.K_r:  # Resetear la figura con R
                poly2 = Polygon([475, 350], [[425, 300], [525, 300], [550, 400], [450, 400]])  # Restaurar posición original
                poly2.rotation = 0  # Asegurarse de que no esté rotada

    # Movimiento del segundo polígono con teclas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        poly2.move(-5, 0)
    if keys[pygame.K_RIGHT]:
        poly2.move(5, 0)
    if keys[pygame.K_UP]:
        poly2.move(0, -5)
    if keys[pygame.K_DOWN]:
        poly2.move(0, 5)

    # **Rotación del polígono con Q y E**
    if keys[pygame.K_q]:
        poly2.rotate(-5)  # Rotar en sentido antihorario
    if keys[pygame.K_e]:
        poly2.rotate(5)   # Rotar en sentido horario

    # Actualizar los AABB después del movimiento o rotación
    box1.update_from_polygon(poly1)
    box2.update_from_polygon(poly2)

    # --- Detección de colisión y visualización ---
    if collision_method == "AABB":
        if poly2.rotation == 0:  # Solo funciona si el polígono NO está rotado
            colliding = box1.intersects(box2)
            text_msg = "AABB: Detecta colisión correctamente" if colliding else "AABB: No hay colisión"
        else:
            colliding = False  # No detectará colisión si el polígono está rotado
            text_msg = "AABB NO funciona con polígonos rotados"
        
        box1.draw((0, 255, 0) if colliding else (255, 0, 0))
        box2.draw((0, 255, 0) if colliding else (255, 0, 0))

    else:
        colliding = poly1.check_collision(poly2)
        text_msg = "SAT: Detecta colisión correctamente" if colliding else "SAT: No hay colisión"

        poly1.draw((0, 255, 0) if colliding else (255, 0, 0))
        poly2.draw((0, 255, 0) if colliding else (255, 0, 0))

    # Mostrar el modo de colisión y mensaje
    text = font.render(f"Modo: {collision_method} (TAB para cambiar, Q/E para rotar, R para resetear)", True, (255, 255, 255))
    message = font.render(text_msg, True, (255, 255, 255))

    screen.blit(text, (20, 20))
    screen.blit(message, (20, 50))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()