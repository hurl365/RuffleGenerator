'''Generate the bottom hemline of the dress using a generated b spline curve in the cartesion coordinate.

The functions and code here are used to generate the bottom hemline 
of the dress, which will be formed by connecting the points using
their x and y coordinate on a 2D plane.

Typical usage example:

hemlineGeneraredBSpline = generateControlPointsCartesian(minRuffleWdith, maxRuffleWidth, minBaseWdith, maxBaseWidth,
                                                minHeight, maxHeight, numFolds, symmetricFold)

Check documentation for the usage of the numbers.
symmetricFold, generate only symmetric folds if set to True.
'''

# Necessary Imports
from geomdl import BSpline
import geomdl
from geomdl.visualization import VisMPL
import random, math # To generate random set of numbers and convert coordinate

# Generate the control points in cartesian coordinate (straight line)
def generateControlPointsCartesian(minRuffleWdith, maxRuffleWidth, minBaseWdith, maxBaseWidth,\
                                    # minDist, maxDist, \ Do not use base point system
                                    minHeight, maxHeight, \
                                    numFolds, symmetricFold, \
                                    randomSeed=None): # Added controlled random
    
    # If no seed is given, generate one
    if randomSeed is None:
        randomSeed = random.SystemRandom().randint(0, 2**32 - 1)

    # Set up controlled randomness, force it to be an int value
    rng = random.Random(int(randomSeed))

    numFolds = int(numFolds) # Force conversion of numFolds
    symmetricFold = bool(symmetricFold) # Force conversion of symmetricFold boolean
    if numFolds <= 0:
        return [] # Return an empty list, if invalid numFolds was given
    if (minRuffleWdith <= 0) or (maxRuffleWidth <= 0) or (maxRuffleWidth < minRuffleWdith):
        return [] # Return an empty list, if invalid ruffle width params were given
    if (minBaseWdith <= 0) or (maxBaseWidth <= 0) or (maxBaseWidth < minBaseWdith):
        return [] # Return an empty list, if invalid base width params were given
    #if (minDist <= 0) or (maxDist <= 0) or (maxDist < minDist):
    #    return [] # Return an empty list, if invalid ruffle dist params were given
    if (minHeight <= 0) or (maxHeight <= 0) or (maxHeight < minHeight):
        return [] # Return an empty list, if invalid ruffle height params were given
    
    # Initialize the list of control points to return
    controlPoints = [[0, 0, 0]] # Force the line to start at (x = 0, y = 0)
    
    # Generate fold by fold
    for foldIter in range(numFolds):
        # Each fold should have one base point on y = 0 line, 
        # offsetted by a randomly generated base width from the last generated point (should be on the line)
        # TODO: this logic could be optimized by just remembering the coord of the last generated point
        lastCtrlPoint = controlPoints[-1]
        lastCtrlPointX = lastCtrlPoint[0] # Get the x-coord of the last generated point
        randBaseWidth = rng.uniform(minBaseWdith, maxBaseWidth)
        basePointX = lastCtrlPointX + randBaseWidth
        # base point's y-coord is always 0

        # With the generated base point, generate the three control points
        randRuffleWidth = rng.uniform(minRuffleWdith, maxRuffleWidth)
        point1X = basePointX - randRuffleWidth
        point2X = basePointX + randRuffleWidth
        point3X = basePointX + randBaseWidth
        # If the the fold do not have to be strictly symmetrical, 
        # just generate a new set of widths for the second and third point
        if not symmetricFold:
            randRuffleWidth = rng.uniform(minRuffleWdith, maxRuffleWidth)
            point2X = basePointX + randRuffleWidth
            randBaseWidth = rng.uniform(minBaseWdith, maxBaseWidth)
            point3X = basePointX + randBaseWidth

        # Different generation depending if the height should be positive or negative
        heightOffset = rng.uniform(minHeight, maxHeight)
        if foldIter % 2 == 1:
            heightOffset = -heightOffset # Use negative height for odd folds
        
        # Now the coordinate for the three points are all generated
        point1 = [point1X, heightOffset, 0]
        point2 = [point2X, heightOffset, 0]
        point3 = [point3X, 0, 0]

        # Add them to the end of the list
        controlPoints.append(point1)
        controlPoints.append(point2)
        controlPoints.append(point3)

    return controlPoints, randomSeed

def testCartesian(numFold = 4, degree = 3, resolution = 0.5):
    # Create a 3-dimensional B-spline Curve
    curve = BSpline.Curve()
    # Set degrees
    curve.degree = degree
    # Set control points
    # curve.ctrlpts = [[5, 0, 0], [0, 10, 0], [15, 10, 0], [10, 0, 0]]
    # Test the points generated for the cartesian coordinate
    ctrlPoints, seedUsed = generateControlPointsCartesian(2, 5, 1, 3, 2, 4, numFold, False)
    #print(ctrlPoints)
    curve.ctrlpts = ctrlPoints
    # Set knot vector
    # Ref: https://www.cl.cam.ac.uk/teaching/1999/AGraphHCI/SMAG/node4.html
    curve.knotvector = geomdl.knotvector.generate(degree, 3 * numFold + 1, clamped=True)
    # Set evaluation delta (controls the number of curve points)
    curve.delta = resolution # Set to smaller to get smoother line
    # Get curve points (the curve will be automatically evaluated)
    curve_points = curve.evalpts
    # Create a visualization configuration instance with no legend, no axes and set the resolution to 120 dpi
    vis_config = VisMPL.VisConfig(legend=False, axes=False, figure_dpi=120)
    # Create a visualization method instance using the configuration above
    vis_obj = VisMPL.VisCurve2D(vis_config)
    # Set the visualization method of the curve object
    curve.vis = vis_obj
    # Plot the curve
    curve.render()
    return curve_points

# Generate the control points in cartesian coordinate (straight line)
# All widths here are treated as degree angles instead
def generateControlPointsPolar(minRuffleWdith, maxRuffleWidth, minBaseWdith, maxBaseWidth, \
                               minHeight, maxHeight, radius, numFolds, symmetricFold, 
                               randomSeed=None): # Added controlled random
    
    # If no seed is given, generate one
    if randomSeed is None:
        randomSeed = random.SystemRandom().randint(0, 2**32 - 1)

    # Set up controlled randomness, force it to be an int value
    rng = random.Random(int(randomSeed))

    numFolds = int(numFolds) # Force conversion of numFolds
    symmetricFold = bool(symmetricFold) # Force conversion of symmetricFold boolean
    if numFolds <= 0:
        return [] # Return an empty list, if invalid numFolds was given
    if (minRuffleWdith <= 0) or (maxRuffleWidth <= 0) or (maxRuffleWidth < minRuffleWdith):
        return [] # Return an empty list, if invalid ruffle width params were given
    if (minBaseWdith <= 0) or (maxBaseWidth <= 0) or (maxBaseWidth < minBaseWdith):
        return [] # Return an empty list, if invalid base width params were given
    if (minHeight <= 0) or (maxHeight <= 0) or (maxHeight < minHeight):
        return [] # Return an empty list, if invalid ruffle height params were given
    # Do not allow any angle greatet than 360
    if (maxRuffleWidth > 360) or (maxBaseWidth > 360):
        return [] # Return an empty list, if invalid width params were given
    if (radius < 0):
        return [] # Return an empty list, if invalid radius was given
    
    # Initialize the list of control points to return
    controlPoints = [[radius, 0]] # Force the line to start at (r = radius, theta = 0)
    
    # Generate fold by fold
    for foldIter in range(numFolds):
        # Each fold should have one base point on y = 0 line, 
        # offsetted by a randomly generated base width from the last generated point (should be on the line)
        # TODO: this logic could be optimized by just remembering the coord of the last generated point
        lastCtrlPoint = controlPoints[-1]
        lastCtrlPointTheta = lastCtrlPoint[1] # Get the angle of the last generated point
        randBaseWidth = rng.uniform(minBaseWdith, maxBaseWidth)
        basePointTheta = lastCtrlPointTheta + randBaseWidth
        # base point's r is always radius

        # With the generated base point, generate the three control points
        randRuffleWidth = rng.uniform(minRuffleWdith, maxRuffleWidth)
        point1Theta = basePointTheta - randRuffleWidth
        point2Theta = basePointTheta + randRuffleWidth
        point3Theta = basePointTheta + randBaseWidth
        # If the the fold do not have to be strictly symmetrical, 
        # just generate a new set of widths for the second and third point
        if not symmetricFold:
            randRuffleWidth = rng.uniform(minRuffleWdith, maxRuffleWidth)
            point2Theta = basePointTheta + randRuffleWidth
            randBaseWidth = rng.uniform(minBaseWdith, maxBaseWidth)
            point3Theta = basePointTheta + randBaseWidth

        # Different generation depending if the height should be positive or negative offset from radius
        heightOffset = rng.uniform(minHeight, maxHeight)
        if foldIter % 2 == 1:
            heightOffset = -heightOffset # Use negative height for odd folds
        point12R = radius+heightOffset
        
        # Now the coordinate for the three points are all generated
        point1 = [point12R, point1Theta]
        point2 = [point12R, point2Theta]
        point3 = [radius, point3Theta]

        # Add them to the end of the list
        controlPoints.append(point1)
        controlPoints.append(point2)
        controlPoints.append(point3)

    # Convert the control points from polar coordinate to cartesian coordinate
    controlPointsCartesian = []
    for point in controlPoints:
        r = point[0]
        theta_value_degrees = point[1]
        x = r * math.cos(math.radians(theta_value_degrees))
        y = r * math.sin(math.radians(theta_value_degrees))
        controlPointsCartesian.append([x, y, 0])

    return controlPointsCartesian, randomSeed

def testPolar(numFold = 4, degree = 3, radius = 20, resolution = 0.5):
    # Create a 3-dimensional B-spline Curve
    curve = BSpline.Curve()
    # Set degrees
    curve.degree = degree
    # Set control points
    # curve.ctrlpts = [[5, 0, 0], [0, 10, 0], [15, 10, 0], [10, 0, 0]]
    # Test the points generated for the polar coordinate
    ctrlPoints, seedUsed = generateControlPointsPolar(6, 8, 4, 5, 1, 3, radius, numFold, False)
    #print(ctrlPoints)
    curve.ctrlpts = ctrlPoints
    # Set knot vector
    # Ref: https://www.cl.cam.ac.uk/teaching/1999/AGraphHCI/SMAG/node4.html
    curve.knotvector = geomdl.knotvector.generate(degree, 3 * numFold + 1, clamped=True)
    # Set evaluation delta (controls the number of curve points)
    curve.delta = resolution # Set to smaller to get smoother line
    # Get curve points (the curve will be automatically evaluated)
    curve_points = curve.evalpts
    # Create a visualization configuration instance with no legend, no axes and set the resolution to 120 dpi
    vis_config = VisMPL.VisConfig(legend=False, axes=False, figure_dpi=120)
    # Create a visualization method instance using the configuration above
    vis_obj = VisMPL.VisCurve2D(vis_config)
    # Set the visualization method of the curve object
    curve.vis = vis_obj
    # Plot the curve
    curve.render()
    return curve_points

# Generate the control points in cartesian coordinate (straight line)
# Generate the control points in cartesian coordinate (straight line)
# All widths here are treated as degree angles instead
def generateControlPointsFullCircle(minRuffleWdith, maxRuffleWidth, minBaseWdith, maxBaseWidth, \
                                    minHeight, maxHeight, radius, numFolds, symmetricFold, 
                                    randomSeed = None, uniformCircle = False): # Added controlled random
    
    # If no seed is given, generate one
    if randomSeed is None:
        randomSeed = random.SystemRandom().randint(0, 2**32 - 1)

    # Set up controlled randomness, force it to be an int value
    rng = random.Random(int(randomSeed))

    numFolds = int(numFolds) # Force conversion of numFolds
    symmetricFold = bool(symmetricFold) # Force conversion of symmetricFold boolean
    if numFolds <= 0:
        return [] # Return an empty list, if invalid numFolds was given
    if (minRuffleWdith <= 0) or (maxRuffleWidth <= 0) or (maxRuffleWidth < minRuffleWdith):
        return [] # Return an empty list, if invalid ruffle width params were given
    if (minBaseWdith <= 0) or (maxBaseWidth <= 0) or (maxBaseWidth < minBaseWdith):
        return [] # Return an empty list, if invalid base width params were given
    if (minHeight <= 0) or (maxHeight <= 0) or (maxHeight < minHeight):
        return [] # Return an empty list, if invalid ruffle height params were given
    # Do not allow any angle greatet than 360
    if (maxRuffleWidth > 360) or (maxBaseWidth > 360):
        return [] # Return an empty list, if invalid width params were given
    if (radius < 0):
        return [] # Return an empty list, if invalid radius was given
    
    # Initialize the list of control points to return
    controlPoints = [[radius, 0]]

    # Get numFolds random angles as base points' angles
    angles = [0] * numFolds
    if uniformCircle:
        averageAngle = 360 / numFolds
        for angleIter in range(1, numFolds):
            randBaseWidth = rng.uniform(averageAngle - minBaseWdith, averageAngle + minBaseWdith)
            angles[angleIter] = angles[angleIter - 1] + randBaseWidth
    else:
        angles = [rng.uniform(0, 360) for _ in range(numFolds)]
        angles.sort() # Sort the generated angle list in place
    
    # Generate fold by fold
    for foldIter in range(numFolds):
        # Each fold should have one base point on y = 0 line, 
        # offsetted by a randomly generated base width from the last generated point (should be on the line)
        # TODO: this logic could be optimized by just remembering the coord of the last generated point
        basePointTheta = angles[foldIter] # Go to the next angle
        # base point's r is always radius

        # With the generated base point, generate the three control points
        randRuffleWidth = rng.uniform(minRuffleWdith, maxRuffleWidth)
        randBaseWidth = rng.uniform(minBaseWdith, maxBaseWidth)
        point1Theta = basePointTheta - randRuffleWidth
        point2Theta = basePointTheta + randRuffleWidth
        point3Theta = basePointTheta + randBaseWidth
        # If the the fold do not have to be strictly symmetrical, 
        # just generate a new set of widths for the second and third point
        if not symmetricFold:
            randRuffleWidth = rng.uniform(minRuffleWdith, maxRuffleWidth)
            point2Theta = basePointTheta + randRuffleWidth
            randBaseWidth = rng.uniform(minBaseWdith, maxBaseWidth)
            point3Theta = basePointTheta + randBaseWidth

        # Different generation depending if the height should be positive or negative offset from radius
        heightOffset = rng.uniform(minHeight, maxHeight)
        if foldIter % 2 == 1:
            heightOffset = -heightOffset # Use negative height for odd folds
        point12R = radius+heightOffset
        
        # Now the coordinate for the three points are all generated
        point1 = [point12R, point1Theta]
        point2 = [point12R, point2Theta]
        if foldIter == numFolds - 1:
            point3Theta = 0 # For the last point, make sure it returns to the starting point
        point3 = [radius, point3Theta]

        # Add them to the end of the list
        controlPoints.append(point1)
        controlPoints.append(point2)
        controlPoints.append(point3)

    # Convert the control points from polar coordinate to cartesian coordinate
    controlPointsCartesian = []
    for point in controlPoints:
        r = point[0]
        theta_value_degrees = point[1]
        x = r * math.cos(math.radians(theta_value_degrees))
        y = r * math.sin(math.radians(theta_value_degrees))
        controlPointsCartesian.append([x, y, 0])

    # Try to smoothen the start and the end
    controlPointsCartesian[-2] = [controlPointsCartesian[0][0] * 2 - controlPointsCartesian[1][0], 
                                  controlPointsCartesian[0][1] * 2 - controlPointsCartesian[1][1], 0]

    return controlPointsCartesian, randomSeed

def testFullCircle(numFold = 4, degree = 3, radius = 20, resolution = 0.5):
    # Create a 3-dimensional B-spline Curve
    curve = BSpline.Curve()
    # Set degrees
    curve.degree = degree
    # Set control points
    # curve.ctrlpts = [[5, 0, 0], [0, 10, 0], [15, 10, 0], [10, 0, 0]]
    # Test the points generated for the polar coordinate
    ctrlPoints, seedUsed = generateControlPointsFullCircle(6, 8, 4, 5, 1, 3, radius, numFold, False, uniformCircle = True)
    #print(ctrlPoints)
    curve.ctrlpts = ctrlPoints
    # Set knot vector
    # Ref: https://www.cl.cam.ac.uk/teaching/1999/AGraphHCI/SMAG/node4.html
    curve.knotvector = geomdl.knotvector.generate(degree, 3 * numFold + 1, clamped=True)
    # Set evaluation delta (controls the number of curve points)
    curve.delta = resolution # Set to smaller to get smoother line
    # Get curve points (the curve will be automatically evaluated)
    curve_points = curve.evalpts
    # Create a visualization configuration instance with no legend, no axes and set the resolution to 120 dpi
    vis_config = VisMPL.VisConfig(legend=False, axes=False, figure_dpi=120)
    # Create a visualization method instance using the configuration above
    vis_obj = VisMPL.VisCurve2D(vis_config)
    # Set the visualization method of the curve object
    curve.vis = vis_obj
    # Plot the curve
    curve.render()
    return curve_points

def getCurvePoints(ctrlPoints, degree = 3, resolution = 0.5):
    curve = BSpline.Curve()
    # Set degrees
    curve.degree = degree
    # Test the points generated for the polar coordinate
    curve.ctrlpts = ctrlPoints
    curve.knotvector = geomdl.knotvector.generate(degree, len(ctrlPoints), clamped=True)
    # Set evaluation delta (controls the number of curve points)
    curve.delta = resolution # Set to smaller to get smoother line
    # Get curve points (the curve will be automatically evaluated)
    curve_points = curve.evalpts
    return curve_points

if __name__ == "__main__":
    testCartesian(numFold = 8, resolution = 0.005)
    testPolar(numFold = 4, resolution = 0.005)
    testFullCircle(numFold = 22, resolution = 0.0001)