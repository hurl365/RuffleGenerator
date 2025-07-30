import numpy as np
from stl import mesh
# To show the model using matplotlib
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import trimesh

from hemline_bspline import testCartesian, testPolar
from hemline_thickness import testThickness

def makeCoordsPositive(coordinates):
    minX = np.min(coordinates[:, 0])
    minY = np.min(coordinates[:, 1])
    # Element-wise addition to all elements in the coordinate to shift the curve to the first quadrant
    coordinates[:, 0] = coordinates[:, 0] - minX
    coordinates[:, 1] = coordinates[:, 1] - minY
    return coordinates

def makeCurtain(topCurve, bottomCurve, height = 5):
    if (topCurve.shape[0] == 0) or (bottomCurve.shape[0]) == 0 or (topCurve.shape[0] != bottomCurve.shape[0]):
        # Do not process if the dimensions do not match
        return None
    # Make faces using indexing of allVertices
    totalFacetGroups = topCurve.shape[0]
    # Combine to two curves into one
    combinedCurve = np.vstack((topCurve, bottomCurve))
    # Make the two curves positive
    combinedCurve = makeCoordsPositive(combinedCurve)
    totalPoints = combinedCurve.shape[0]
    height = np.zeros((totalPoints, 1)) + height
    bottomCurve = np.hstack((combinedCurve, np.zeros((totalPoints, 1))))
    topCurve = np.hstack((combinedCurve, height))
    # Combine the top curve and bottom curve
    allVertices = np.vstack((bottomCurve, topCurve))
    # Swap indexing
    allVertices[:, [1, 2]] = allVertices[:, [2, 1]]
    allFaces = []
    # Constants used in loop
    n = totalFacetGroups
    nn = totalPoints
    # Add 2 leftmost faces
    allFaces.append([0, n+nn, n])
    allFaces.append([n+nn, 0, nn])
    for x in range(n - 1): # The last one on the other side ignored
       # Top and bottom pieces
       allFaces.append([x, x+n+1, x+1]) # Bottom piece 1
       allFaces.append([x, x+n, x+n+1]) # Bottom piece 2
       allFaces.append([x+nn, x+1+nn, x+n+1+nn]) # Top piece 3
       allFaces.append([x+nn, x+n+nn+1, x+n+nn]) # Top piece 4
       # Side walls (right)
       allFaces.append([x, x+1, x+nn+1]) # Side wall piece 5
       allFaces.append([x, x+nn+1, x+nn]) # Side wall piece 6
       #allFaces.append([x+1, x+n+1, x+nn+1]) # Side wall piece 7
       #allFaces.append([x+n+1, x+nn+n+1, x+nn+1]) # Side wall piece 8
       # Side walls (left)
       allFaces.append([x+n+1, x+nn+n, x+nn+n+1]) # Side wall piece 9
       allFaces.append([x+n+1, x+n, x+nn+n]) # Side wall piece 10
       #allFaces.append([x, x+nn, x+nn+n]) # Side wall piece 11
       #allFaces.append([x, x+n+nn, x+n]) # Side wall piece 12
    # Add 2 rightmost faces
    allFaces.append([n-1, nn-1, n+nn-1])
    allFaces.append([nn-1, nn+nn-1, n+nn-1])
    return np.array(allVertices), np.array(allFaces)

def makeSTL(vertices, faces, filename='curtain.stl', dir='.'):
    # Create the mesh
    generatedMesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            generatedMesh.vectors[i][j] = vertices[f[j], :]

    # Write the mesh to an STL file
    generatedMesh.save(dir+"/"+filename)

def verifyMesh(filename='curtain.stl', dir='.'):
    mesh = trimesh.load(dir+"/"+filename)
    # Check for self-intersections
    if not mesh.is_watertight or not mesh.is_volume:
        print("Mesh is not watertight or manifold, attempting repair...")
        # Attempt to repair the mesh
        # This might involve filling holes, removing non-manifold edges, etc.
        # The specific repair method depends on the nature of the error.
        # For self-intersections, you might need more advanced tools or manual intervention.
        # Example: Simple repair attempt (may not fix all intersection types)
        mesh.fill_holes()
        mesh.remove_degenerate_faces()
        mesh.remove_duplicate_faces()
        mesh.remove_invalid() # Removes non-manifold components and other issues

        # Export the repaired mesh
        mesh.export(dir+"/"+filename)
        #print("Repair attempt completed. Check '{}'.".format(filename))
    #else:
        #print("Mesh is already watertight and manifold.")

def testMesh():
    #sampleHemline = np.array(testCartesian(numFold = 8, resolution = 0.01))
    sampleHemline = np.array(testPolar(numFold = 20, resolution = 0.0001))
    plusDelta, minusDelta = testThickness(sampleHemline, thickness = 0.5)
    generatedVertices, generatedFaces = makeCurtain(plusDelta, minusDelta, height = 5)
    makeSTL(generatedVertices, generatedFaces, filename='curtain.stl', dir='.')
    verifyMesh(filename='curtain.stl', dir='.')

if __name__ == "__main__":
    testMesh()