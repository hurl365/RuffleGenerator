import numpy as np
from stl import mesh
# To show the model using matplotlib
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import trimesh

from hemline_bspline import generateControlPointsFullCircle, generateControlPointsPolar, getCurvePoints, testCartesian, testPolar, testFullCircle
from hemline_thickness import testThickness, thickenHemline

def makeCoordsPositive(coordinates):
    minX = np.min(coordinates[:, 0])
    minY = np.min(coordinates[:, 1])
    # Element-wise addition to all elements in the coordinate to shift the curve to the first quadrant
    coordinates[:, 0] = coordinates[:, 0] - minX
    coordinates[:, 1] = coordinates[:, 1] - minY
    return coordinates

def makeCurtain(outsideCurve, insideCurve, height = 5):
    if (outsideCurve.shape[0] == 0) or (insideCurve.shape[0]) == 0 or (outsideCurve.shape[0] != insideCurve.shape[0]):
        # Do not process if the dimensions do not match
        return None
    # Make faces using indexing of allVertices
    totalFacetGroups = outsideCurve.shape[0]
    # Combine to two curves into one
    combinedCurve = np.vstack((outsideCurve, insideCurve))
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

def makeCurtainFullCircle(outsideCurve, insideCurve, height = 5):
    if (outsideCurve.shape[0] == 0) or (insideCurve.shape[0]) == 0 or (outsideCurve.shape[0] != insideCurve.shape[0]):
        # Do not process if the dimensions do not match
        return None
    # Make faces using indexing of allVertices
    totalFacetGroups = outsideCurve.shape[0]
    # Combine to two curves into one
    combinedCurve = np.vstack((outsideCurve, insideCurve))
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
    return np.array(allVertices), np.array(allFaces)

def makeCape(bottomOutCurve, bottomInCurve, topOutCurve, topInCurve, height = 5):
    if (bottomOutCurve.shape[0] == 0) or (bottomInCurve.shape[0] == 0) \
        or (topOutCurve.shape[0] == 0) or (topInCurve.shape[0] == 0) \
        or (bottomOutCurve.shape[0] != bottomInCurve.shape[0]) \
        or (bottomOutCurve.shape[0] != topOutCurve.shape[0]) \
        or (bottomOutCurve.shape[0] != topInCurve.shape[0]):
        # Do not process if the dimensions do not match or are invalid
        return None
    # Make faces using indexing of allVertices
    totalFacetGroups = bottomOutCurve.shape[0]
    # Combine to two curves into one
    combinedBottomCurve = np.vstack((bottomOutCurve, bottomOutCurve))
    combinedTopCurve = np.vstack((topOutCurve, topInCurve))
    # Make the two curves positive
    #combinedBottomCurve = makeCoordsPositive(combinedBottomCurve)
    #combinedTopCurve = makeCoordsPositive(combinedTopCurve)
    totalPoints = combinedBottomCurve.shape[0]
    height = np.zeros((totalPoints, 1)) + height
    bottomCurve = np.hstack((combinedBottomCurve, np.zeros((totalPoints, 1))))
    topCurve = np.hstack((combinedTopCurve, height))
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

def makeSkirt(bottomOutCurve, bottomInCurve, topOutCurve, topInCurve, height = 5):
    if (bottomOutCurve.shape[0] == 0) or (bottomInCurve.shape[0] == 0) \
        or (topOutCurve.shape[0] == 0) or (topInCurve.shape[0] == 0) \
        or (bottomOutCurve.shape[0] != bottomInCurve.shape[0]) \
        or (bottomOutCurve.shape[0] != topOutCurve.shape[0]) \
        or (bottomOutCurve.shape[0] != topInCurve.shape[0]):
        # Do not process if the dimensions do not match or are invalid
        return None
    # Make faces using indexing of allVertices
    totalFacetGroups = bottomOutCurve.shape[0]
    # Combine to two curves into one
    combinedBottomCurve = np.vstack((bottomOutCurve, bottomOutCurve))
    combinedTopCurve = np.vstack((topOutCurve, topInCurve))
    # Make the two curves positive
    #combinedBottomCurve = makeCoordsPositive(combinedBottomCurve)
    #combinedTopCurve = makeCoordsPositive(combinedTopCurve)
    totalPoints = combinedBottomCurve.shape[0]
    height = np.zeros((totalPoints, 1)) + height
    bottomCurve = np.hstack((combinedBottomCurve, np.zeros((totalPoints, 1))))
    topCurve = np.hstack((combinedTopCurve, height))
    # Combine the top curve and bottom curve
    allVertices = np.vstack((bottomCurve, topCurve))
    # Swap indexing
    allVertices[:, [1, 2]] = allVertices[:, [2, 1]]
    allFaces = []
    # Constants used in loop
    n = totalFacetGroups
    nn = totalPoints
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
        print("Mesh {} is not watertight or manifold, attempting repair...".format(filename))
        # Attempt to repair the mesh
        trimesh.repair.broken_faces(mesh, color=None)
        trimesh.repair.fill_holes(mesh)
        trimesh.repair.fix_inversion(mesh, multibody=False)
        trimesh.repair.fix_normals(mesh, multibody=False)
        trimesh.repair.fix_winding(mesh)
        mesh.export(dir+"/"+filename)
        print("Repair attempt completed. Check '{}'.".format(filename))
    else:
        print("Mesh {} is already watertight and manifold.".format(filename))

def testMesh():
    # Test Cartesian or polar
    #sampleHemline = np.array(testCartesian(numFold = 8, resolution = 0.01))
    sampleHemline = np.array(testPolar(numFold = 20, resolution = 0.0001))
    plusDelta, minusDelta = testThickness(sampleHemline, thickness = 0.5)
    generatedVertices, generatedFaces = makeCurtain(plusDelta, minusDelta, height = 5)
    makeSTL(generatedVertices, generatedFaces, filename='curtain.stl', dir='.')
    verifyMesh(filename='curtain.stl', dir='.')
    # Test Full Circle
    sampleHemline = np.array(testFullCircle(numFold = 20, resolution = 0.0001))
    plusDelta, minusDelta = testThickness(sampleHemline, thickness = 0.5)
    generatedVertices, generatedFaces = makeCurtainFullCircle(plusDelta, minusDelta, height = 5)
    makeSTL(generatedVertices, generatedFaces, filename='fullCircle.stl', dir='.')
    verifyMesh(filename='fullCircle.stl', dir='.')
    
def testSkirtsMesh():
    # Test skirt generation
    bottomCtrlPoints, randomSeed = generateControlPointsFullCircle( \
                    minRuffleWdith=6, maxRuffleWidth=8, minBaseWdith=4, maxBaseWidth=5, \
                    minHeight=1, maxHeight=3, radius=20, numFolds=20, symmetricFold=False, 
                    randomSeed = None, uniformCircle = True)
    bottomHemline = np.array(getCurvePoints(bottomCtrlPoints, degree = 3, resolution = 0.0005))
    bottomPlusDelta, bottomMinusDelta = thickenHemline(bottomHemline, thickness = 0.5)
    topCtrlPoints, randomSeed = generateControlPointsFullCircle( \
                    minRuffleWdith=6, maxRuffleWidth=8, minBaseWdith=4, maxBaseWidth=5, \
                    minHeight=1, maxHeight=3, radius=6, numFolds=20, symmetricFold=False, 
                    randomSeed = randomSeed, uniformCircle = True)
    topHemline = np.array(getCurvePoints(topCtrlPoints, degree = 3, resolution = 0.0005))
    topPlusDelta, topMinusDelta = thickenHemline(topHemline, thickness = 0.2)
    generatedVertices, generatedFaces = makeSkirt(bottomOutCurve=bottomPlusDelta, \
                                                bottomInCurve=bottomMinusDelta, \
                                                topOutCurve=topPlusDelta, \
                                                topInCurve=topMinusDelta, height = 35)
    makeSTL(generatedVertices, generatedFaces, filename='skirt.stl', dir='.')
    verifyMesh(filename='skirt.stl', dir='.')

    # Test cape generation
    bottomCtrlPoints, randomSeed = generateControlPointsPolar( \
                    minRuffleWdith=10, maxRuffleWidth=16, minBaseWdith=5, maxBaseWidth=8, \
                    minHeight=1, maxHeight=3, radius=20, numFolds=10, symmetricFold=False, 
                    randomSeed = None)
    bottomHemline = np.array(getCurvePoints(bottomCtrlPoints, degree = 3, resolution = 0.0005))
    bottomPlusDelta, bottomMinusDelta = thickenHemline(bottomHemline, thickness = 0.5)
    topCtrlPoints, randomSeed = generateControlPointsPolar( \
                    minRuffleWdith=10, maxRuffleWidth=16, minBaseWdith=5, maxBaseWidth=8, \
                    minHeight=1, maxHeight=3, radius=10, numFolds=10, symmetricFold=False, 
                    randomSeed = randomSeed)
    topHemline = np.array(getCurvePoints(topCtrlPoints, degree = 3, resolution = 0.0005))
    topPlusDelta, topMinusDelta = thickenHemline(topHemline, thickness = 0.2)
    generatedVertices, generatedFaces = makeCape(bottomOutCurve=bottomPlusDelta, \
                                                bottomInCurve=bottomMinusDelta, \
                                                topOutCurve=topPlusDelta, \
                                                topInCurve=topMinusDelta, height = 35)
    makeSTL(generatedVertices, generatedFaces, filename='cape.stl', dir='.')
    verifyMesh(filename='cape.stl', dir='.')

if __name__ == "__main__":
    #testMesh()
    testSkirtsMesh()