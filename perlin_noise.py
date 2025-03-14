import noise
import numpy as np
import matplotlib.pyplot as plt

# Parámetros del mapa de ruido
width = 100  # Ancho del mapa
height = 100  # Alto del mapa
scale = 20.0  # Escala del ruido

# Crear una matriz para almacenar los valores de ruido
mapa = np.zeros((width, height))

# Generar Perlin Noise en 2D
for y in range(height):
    for x in range(width):
        nx = x / scale
        ny = y / scale
        mapa[x][y] = noise.pnoise2(nx, ny, octaves=6, persistence=0.5, lacunarity=2.0)

# Mostrar el mapa generado con colores más variados
plt.imshow(mapa, cmap="jet")  #"jet", "viridis", "plasma"
plt.colorbar()
plt.show()
