import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def setMatrix(n, k, m):
    matrix = np.zeros((n, n))
    
    for i in range(n):
        if i > 0:
            matrix[i, i-1] = -k[i] / m[i]
        matrix[i, i] = (k[i] + k[i+1]) / m[i]
        if i < n-1:
            matrix[i, i+1] = -k[i+1] / m[i]  
    
    return matrix

def simulation(n, k, m, mode):
    matrix = setMatrix(n, k, m)
    
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    
    frequency = np.sqrt(eigenvalues[mode])
    coordinate = eigenvectors[:, mode]
    
    return frequency, coordinate

def animation(n, k, m, mode):
    frequency, coordinate = simulation(n, k, m, mode)
    
    fig, ax = plt.subplots()
    ax.set_xlim(0, n + 2)
    ax.set_ylim(-2, 2)

    mass_texts = [ax.text(i + 0.75, 0.15, str(mass), ha='center', fontsize=12) for i, mass in enumerate(m)]

    time_step = 0.05
    t_max = 10

    def update(frame):
        t = frame * time_step
        positions = []
        for i in range(n):
            displacement = coordinate[i] * np.cos(frequency * t)
            positions.append(displacement)

        for i, mass_text in enumerate(mass_texts):
            mass_text.set_position((i + 0.75, positions[i] + 0.15))

        return mass_texts

    animate = FuncAnimation(fig, update, frames=int(t_max / time_step), blit=True, interval=50, repeat=True)

    plt.title(f"Mode {mode + 1} Oscillation")
    plt.show()

n = int(input("Enter number of masses: "))
m = [float(input(f"Enter mass {i+1}: ")) for i in range(n)]
k = [float(input(f"Enter spring constant k{i+1}: ")) for i in range(n + 1)]
mode = int(input("Enter mode (0 for in-phase, 1 for out-of-phase, etc.): "))

animation(n, k, m, mode)
