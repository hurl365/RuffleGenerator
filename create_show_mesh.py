# Ref:
# https://medium.com/@wide4head/creating-step-stl-files-directly-from-python-0f4aaf01cb5f
# https://pypi.org/project/numpy-stl/?source=post_page-----0f4aaf01cb5f---------------------------------------
import numpy as np
from stl import mesh
# To show the model using matplotlib
from mpl_toolkits import mplot3d
from matplotlib import pyplot

# Create 8 vertices of the cube (just the points in the 3D space)
vertices = np.array([
    [0, 0, 0],
    [100, 0, 0],
    [100, 100, 0],
    [0, 100, 0],
    [0, 0, 100],
    [100, 0, 100],
    [100, 100, 100],
    [0, 100, 100]
])

# Create 12 triangles of the cube (triplets of indices of the previous array, connect vertices to form triangles)
faces = np.array([
    [1, 3, 2],
    [0, 3, 1],
    [0, 4, 7],
    [0, 7, 3],
    [4, 5, 6],
    [4, 6, 7],
    [5, 1, 2],
    [5, 2, 6],
    [2, 3, 6],
    [3, 7, 6],
    [0, 1, 5],
    [0, 5, 4]
])

# Create the mesh
cube_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cube_mesh.vectors[i][j] = vertices[f[j], :]

# Write the mesh to an STL file
cube_mesh.save('cube.stl')

# Create a new plot
figure = pyplot.figure()
axes = figure.add_subplot(projection='3d')

# Load the STL files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('cube.stl')
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

# Auto scale to the mesh size
scale = your_mesh.points.flatten()
axes.auto_scale_xyz(scale, scale, scale)

# Show the plot to the screen
pyplot.show()