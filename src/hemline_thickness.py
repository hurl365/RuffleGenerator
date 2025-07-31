import matplotlib.pyplot as plt
import numpy as np
import math

from hemline_bspline import testCartesian, testPolar, testFullCircle # Test code-generated line

def thickenHemline(hemline, thickness = 0.5):
    plusDelta = []
    minusDelta = []
    hemlineX = hemline[:, 0]
    hemlineY = hemline[:, 1]
    # Handle the first point using only its coord and the second point's coordinate
    nextPointX = hemlineX[1]
    currPointX = hemlineX[0]
    nextPointY = hemlineY[1]
    currPointY = hemlineY[0]
    beta = None
    beta = math.atan2((nextPointY - currPointY), (nextPointX - currPointX))
    deltaAngle = beta + math.pi/2
    # Calculate delta from the current point
    deltaX = thickness * math.cos(deltaAngle)
    deltaY = thickness * math.sin(deltaAngle)
    # Append the deviated point's coordinates
    plusDelta.append([currPointX + deltaX, currPointY + deltaY])
    minusDelta.append([currPointX - deltaX, currPointY - deltaY])
    # Skip the first and last point's thickening in angle approximation method
    for pointIter in range(1, hemline.shape[0] - 1):
        # Get the current point's coordinate and the neighboring points' coordinates
        prevPointX = hemlineX[pointIter - 1]
        nextPointX = hemlineX[pointIter + 1]
        currPointX = hemlineX[pointIter]
        prevPointY = hemlineY[pointIter - 1]
        nextPointY = hemlineY[pointIter + 1]
        currPointY = hemlineY[pointIter]
        prevAngle = math.atan2((prevPointY - currPointY), (prevPointX - currPointX))
        nextAngle = math.atan2((nextPointY - currPointY), (nextPointX - currPointX))
        openAngle = prevAngle - nextAngle
        deltaAngle = nextAngle + openAngle / 2.0
        # Calculate delta from the current point
        deltaX = thickness * math.cos(deltaAngle)
        deltaY = thickness * math.sin(deltaAngle)
        if openAngle < 0:
            deltaX = -deltaX
            deltaY = -deltaY
        # Append the deviated point's coordinates
        plusDeltaCoord = [currPointX + deltaX, currPointY + deltaY]
        minusDeltaCoord = [currPointX - deltaX, currPointY - deltaY]
        plusDelta.append(plusDeltaCoord)
        minusDelta.append(minusDeltaCoord)
    # Handle the last point using only its coord and the second last point's coordinate
    prevPointX = hemlineX[hemline.shape[0] - 2]
    currPointX = hemlineX[hemline.shape[0] - 1]
    prevPointY = hemlineY[hemline.shape[0] - 2]
    currPointY = hemlineY[hemline.shape[0] - 1]
    beta = math.atan2((prevPointY - currPointY), (prevPointX - currPointX))
    deltaAngle = beta - math.pi/2
    # Calculate delta from the current point
    deltaX = thickness * math.cos(deltaAngle)
    deltaY = thickness * math.sin(deltaAngle)
    # Append the deviated point's coordinates
    plusDelta.append([currPointX + deltaX, currPointY + deltaY])
    minusDelta.append([currPointX - deltaX, currPointY - deltaY])
    return np.array(plusDelta), np.array(minusDelta)

def testThickness(testHemline, thickness = 0.5):
    plusDelta, minusDelta = thickenHemline(testHemline, thickness)
    hemlineX = testHemline[:, 0]
    hemlineY = testHemline[:, 1]
    plt.plot(hemlineX, hemlineY, color='black', linestyle='--', linewidth=2, marker='o')
    plt.plot(plusDelta[:, 0], plusDelta[:, 1], color='red', linestyle='--', linewidth=2, marker='o')
    plt.plot(minusDelta[:, 0], minusDelta[:, 1], color='blue', linestyle='--', linewidth=2, marker='o')
    plt.title("Thickness Test Plot")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.show()
    return plusDelta, minusDelta

if __name__ == "__main__":
    sampleHemline = np.array(testCartesian(numFold = 8, resolution = 0.01))
    sampleHemline = np.array(testPolar(numFold = 4, resolution = 0.01))
    sampleHemline = np.array(testFullCircle(numFold = 20, resolution = 0.0001))
    testThickness(sampleHemline, thickness = 0.5)