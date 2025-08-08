# Helper functions for main to aggregate functionalities of other scripts
import numpy as np
from stl import mesh
import trimesh

from src.hemline_bspline import generateControlPointsFullCircle, generateControlPointsPolar, getCurvePoints, testCartesian, testPolar, testFullCircle
from src.create_mesh import makeSkirt
from src.hemline_thickness import thickenHemline

# Skirt generation
def generateSkirt():
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
   
    # Create the mesh
    generatedMesh = trimesh.Trimesh(vertices=generatedVertices, faces=generatedFaces, process=True)
    # Check for mesh validity
    if not generatedMesh.is_watertight or not generatedMesh.is_volume:
        # Attempt to repair the mesh
        trimesh.repair.broken_faces(generatedMesh, color=None)
        trimesh.repair.fill_holes(generatedMesh)
        trimesh.repair.fix_inversion(generatedMesh, multibody=False)
        trimesh.repair.fix_normals(generatedMesh, multibody=False)
        trimesh.repair.fix_winding(generatedMesh)
    
    return generatedMesh