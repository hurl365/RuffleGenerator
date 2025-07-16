'''Generate the bottom hemline of the dress.

The functions and code here are used to generate the bottom hemline 
of the dress, which will be formed by connecting the points using
their x and y coordinate on a 2D plane.

Typical usage example:

hemlineGenerared = generateHemline(pairOfFolds, minFoldRadius, maxFoldRadius,
                                    numCurvePoints)
'''
# necessary imports
import random, math

def generateHemline(pairOfFolds, minFoldRadius, maxFoldRadius,
                    numCurvePoints) -> list:
    '''generate the points to form the hemline (without width/thickness)

    Using the given input to create points to form the hemline that does not
    have a thickness.

    Args:
        pairOfFolds:
            The number of pairs of folds to generate for this hemline.
            Minimum is 1, and it must be a positive integer.
        minFoldRadius:
            The minimum value of the radius for each fold
            Must be a positive number. 0 if there is no limit.
        maxFoldRadius:
            The maximum value of the radius for each fold
            Must be a positive number. 0 if there is no limit.
        numCurvePoints:
            The number of point to generate for each fold (circle segment)
            Minimum is 2, must be a positive integer.
    
    Returns:
        circleCenters:
            The center of circles that is used to generate each point on the hemline.
            It is a list of tuples, each representing a center of circle's corrdinate.
        hemlineGenerated:
            A list of list of tuples, the outer list contains the inner lists of tuples,
            each inner list is representing the points to form a fold, and each tuple
            represents the coordinate of a point.
    '''
    hemlineGenerated = []
    circleRadii = generateCircleRadii(pairOfFolds, minFoldRadius, maxFoldRadius)
    circleCenters = generateCircleCenters(pairOfFolds, circleRadii)

def generateCircleRadii(pairOfFolds, minFoldRadius, maxFoldRadius) -> list:
    # Adjust the values if necessary, make sure input is appropriate
    if maxFoldRadius == 0: # if there is no upper bound for fold radius
        maxFoldRadius = float('inf') # the upper bound if inifinity
    if minFoldRadius < 0: # make sure the lower bound is not negative
        minFoldRadius = 0
    circleRadii = [] # the list of circle radii
    for centerCount in range(0, pairOfFolds * 2):
        # Randomly generate the next radius in the given range and append to list
        nextCircleRadius = random.uniform(minFoldRadius, maxFoldRadius)
        circleRadii.append(nextCircleRadius)
    return circleRadii

def generateCircleCenters(pairOfFolds, circleRadii) -> list:
    circleCenters = [] # store the generated circle centers
    # Find the first circle's center
    prevRadius = circleRadii[0]
    prevY = random.uniform(0, prevRadius * 2) # find a random starting point
    prevX = 0 # starting from x = 0 (leftmost)
    # Use trig to calculate the change in x and y coordinate
    [deltaX, deltaY] = getDeltaToNextCircleCenter(prevRadius)
    currX = prevX + deltaX # go to the right of the origin for the first point
    currY = prevY + deltaY
    prevX = currX # record the previously calculated circle center coordinate
    prevY = currY
    circleCenters.append((currX, currY)) # Append the tuple (coordinate) to the list
    for centerCount in range(1, pairOfFolds * 2):
        # Amount of shift = radius for the previous fold + radius for current fold
        currRadius = circleRadii[centerCount]
        deltaRadius = prevRadius + currRadius
        # Use trig to calculate the change in x and y coordinate
        [deltaX, deltaY] = getDeltaToNextCircleCenter(deltaRadius)
        currX = prevX + deltaX # keep going right for the next point
        currY = prevY + deltaY
        prevX = currX
        prevY = currY
        prevRadius = currRadius
        circleCenters.append((currX, currY)) # Append the tuple to the list
    return circleCenters

def getDeltaToNextCircleCenter(radius) -> list:
    # randomly generate the angle of projection to the next point
    projectAngle = random.uniform(-math.pi / 2, math.pi / 2)
    # find the change in x and y changes to get to the next point
    deltaX = radius * math.cos(projectAngle)
    deltaY = radius * math.sin(projectAngle)
    return [deltaX, deltaY]

def sanityTest():
    print("******Executing sanity test: getDeltaToNextCircleCenter******")
    print(getDeltaToNextCircleCenter(5))
    print("******Executing sanity test: generateCircleRadii******")
    print(generateCircleRadii(2, 1, 9))
    print("******Executing sanity test: generateCircleCenters******")
    print(generateCircleCenters(2, [1, 9, 3, 7]))

if __name__ == '__main__':
    print("******Executing sanity tests******")
    sanityTest()