import math

# rotates a vector clockwise
def rotate_vector(vector, angle):
    x = vector['x']
    y = vector['y']
    cosa = math.cos(angle)
    sina = math.sin(angle)

    result = dict(x = x * cosa - y * sina, y = x * sina + y * cosa)
    return result

# find the angle between any two points
def get_angle(point1, point2):
    opp = math.fabs(point1['x'] - point2['x'])
    adj = math.fabs(point1['y'] - point2['y'])
    theta = math.atan2(opp, adj)

    return theta

