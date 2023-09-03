'''Generate the bottom hemline of the dress.

The functions and code here are used to generate the bottom hemline 
of the dress, which will be formed by connecting the points using
their x and y coordinate on a 2D plane.

Typical usage example:

hemlineGenerared = generateHemline(pairOfFolds, minFoldRadius, maxFoldRadius,
                                    maxHeight, maxWidth, numCurvePoints)
'''
# necessary imports
import random

def generateHemline(pairOfFolds, minFoldRadius, maxFoldRadius,
                    maxHeight, maxWidth, numCurvePoints) -> list:
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
        maxHeight:
            The maximum y-coordinate value for the points generated
            Must be a positive number. 0 if there is no limit.
        maxWidth:
            The maximum x-coordinate value for the points generated
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
    circleCenters = generateCircleCenters(pairOfFolds, minFoldRadius, maxFoldRadius,
                                          maxHeight, maxWidth)

def generateCircleCenters(pairOfFolds, minFoldRadius, maxFoldRadius,
                                          maxHeight, maxWidth) -> list:
    prevY = random.uniform(0, maxHeight) # find a random starting point
    prevX = 0 # starting from x = 0 (leftmost)
    for centerCount in range [0, pairOfFolds * 2 - 1]:
        [deltaX, deltaY] = getDeltaToNextCircleCenter(prevX, prevY, minFoldRadius, 
                                                      maxFoldRadius, maxHeight, maxWidth)
        currX = prevX + deltaX # keep going right for the next point
        currY = prevY + deltaY
        prevX = currX
        prevY = currY

