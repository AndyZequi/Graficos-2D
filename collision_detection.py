import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.widgets import Button
import math

# --- FUNCIONES PARA AABB ---
def check_aabb_collision(A, B):
    """Detecta colisión entre dos AABB (rectángulos alineados a los ejes)"""
    return not (A[0] > B[0] + B[2] or A[0] + A[2] < B[0] or A[1] > B[1] + B[3] or A[1] + A[3] < B[1])

def draw_aabb(ax, A, B, collision):
    """Dibuja los AABB"""
    colorA = 'red' if collision else 'black'
    colorB = 'blue' if collision else 'black'
    ax.add_patch(patches.Rectangle((A[0], A[1]), A[2], A[3], linewidth=2, edgecolor=colorA, facecolor='none'))
    ax.add_patch(patches.Rectangle((B[0], B[1]), B[2], B[3], linewidth=2, edgecolor=colorB, facecolor='none'))

# --- FUNCIONES PARA SAT ---
def project_polygon(polygon, axis):
    """Proyecta un polígono sobre un eje"""
    projections = [np.dot(vertex, axis) for vertex in polygon]
    return [min(projections), max(projections)]

def check_sat_collision(polygon1, polygon2):
    """Detecta colisión entre dos polígonos usando SAT"""
    for polygon in [polygon1, polygon2]:
        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]
            edge = np.array([p2[0] - p1[0], p2[1] - p1[1]])
            axis = np.array([-edge[1], edge[0]])  # Eje perpendicular

            projection1 = project_polygon(polygon1, axis)
            projection2 = project_polygon(polygon2, axis)

            if projection1[1] < projection2[0] or projection2[1] < projection1[0]:
                return False  # No hay intersección en esta proyección
    return True

def draw_sat(ax, polygon1, polygon2, collision):
    """Dibuja los polígonos para SAT"""
    color1 = 'red' if collision else 'black'
    color2 = 'blue' if collision else 'black'
    ax.add_patch(patches.Polygon(polygon1, closed=True, edgecolor=color1, facecolor='none', linewidth=2))
    ax.add_patch(patches.Polygon(polygon2, closed=True, edgecolor=color2, facecolor='none', linewidth=2))

# --- ROTACIÓN DE POLÍGONOS ---
def rotate_polygon(polygon, angle, center):
    """Rota un polígono en torno a un punto"""
    angle = np.radians(angle)
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    
    rotated_polygon = []
    for vertex in polygon:
        x, y = vertex
        cx, cy = center
        x -= cx
        y -= cy
        x_new = x * cos_theta - y * sin_theta
        y_new = x * sin_theta + y * cos_theta
        rotated_polygon.append((x_new + cx, y_new + cy))

    return np.array(rotated_polygon)

# --- FUNCIÓN PRINCIPAL ---
def update_plot():
    """Dibuja y actualiza la visualización con AABB o SAT"""
    ax.clear()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal', adjustable='box')

    if use_aabb:
        collision = check_aabb_collision(A, B)
        draw_aabb(ax, A, B, collision)
        ax.set_title("AABB: " + ("Colisión detectada" if collision else "Sin colisión"), fontsize=14, color='red' if collision else 'green')
    else:
        global rotated_polygon1
        rotated_polygon1 = rotate_polygon(polygon1, rotation_angle, (4, 4))  # Rota el primer polígono
        collision = check_sat_collision(rotated_polygon1, polygon2)
        draw_sat(ax, rotated_polygon1, polygon2, collision)
        ax.set_title("SAT: " + ("Colisión detectada" if collision else "Sin colisión"), fontsize=14, color='red' if collision else 'green')

    plt.draw()

def toggle_algorithm(event):
    """Cambia entre AABB y SAT"""
    global use_aabb
    use_aabb = not use_aabb
    update_plot()

def rotate_left(event):
    """Rota la figura en sentido antihorario"""
    global rotation_angle
    rotation_angle += 10
    update_plot()

def rotate_right(event):
    """Rota la figura en sentido horario"""
    global rotation_angle
    rotation_angle -= 10
    update_plot()

# --- DATOS ---
use_aabb = True  # Variable para alternar entre AABB y SAT
rotation_angle = 0  # Ángulo de rotación inicial

# Rectángulos para AABB (x, y, ancho, alto)
A = (1, 3, 3, 3)
B = (5, 5, 3, 3)

# Polígonos para SAT
polygon1 = np.array([(2, 2), (4, 5), (6, 3)])
polygon2 = np.array([(5, 4), (7, 7), (9, 5)])
rotated_polygon1 = polygon1.copy()  # Inicialmente sin rotación

# --- CREAR FIGURA ---
fig, ax = plt.subplots()
fig.canvas.manager.set_window_title('Colisiones AABB vs SAT')

# Botón para alternar entre AABB y SAT
button_ax = fig.add_axes([0.75, 0.05, 0.15, 0.05])
button = Button(button_ax, 'Alternar')
button.on_clicked(toggle_algorithm)

# Botón para rotar a la izquierda
button_ax_left = fig.add_axes([0.55, 0.05, 0.1, 0.05])
button_left = Button(button_ax_left, '⟲')
button_left.on_clicked(rotate_left)

# Botón para rotar a la derecha
button_ax_right = fig.add_axes([0.65, 0.05, 0.1, 0.05])
button_right = Button(button_ax_right, '⟳')
button_right.on_clicked(rotate_right)

update_plot()
plt.show()