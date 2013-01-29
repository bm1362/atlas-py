import math

# rotates a vector clockwise
def rotate_vector(vector, angle):
    x = vector['x']
    y = vector['y']
    cosa = math.cos(angle)
    sina = math.sin(angle)

    result = dict(x = x * cosa - y * sina, y = x * sina + y * cosa)
    return result