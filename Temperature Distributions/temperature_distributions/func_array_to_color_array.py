from numpy import array, uint8

def array_to_color_array(originalArr, gradientObj):
    """converts a two-dimensional array into an array of RGB triples according to a range determined by the
    minimum and maximum values of the array and the specified gradient"""

    flatArr = originalArr.flatten()
    minX, maxX = min(flatArr), max(flatArr)

    percentArr = (originalArr - minX) / (maxX - minX)
    colorFunc = lambda percent: gradientObj.percentColor(percent)

    colorArr = []
    for i in range(percentArr.shape[0]):
        colorArr.append([])
        for j in range(percentArr.shape[1]):
            colorArr[i].append(colorFunc(percentArr[i][j]))
    colorArr = array(colorArr, dtype=uint8)

    return colorArr