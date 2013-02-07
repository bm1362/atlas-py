"""
vector2.py: Contains a collection of functions that aid in the various movements of the entities in our world.
"""

import math

# rotates a vector clockwise
def rotate_vector(vector, angle):
    x = vector['x']
    y = vector['y']
    cosa = math.cos(angle * math.pi / 180)
    sina = math.sin(angle * math.pi / 180)

    result = dict(x = x * cosa - y * sina, y = x * sina + y * cosa)
    return result

# Finds the angle that passes through any two points relative to the x-axis
def get_angle(point1, point2):
    opp = math.fabs(point1['x'] - point2['x'])
    adj = math.fabs(point1['y'] - point2['y'])
    theta = math.atan2(opp, adj)

    return theta

def angle_between(v1, v2):
	dot = dot_product(v1, v2)
	origin = dict(x=0,y=0)
	d1 = distance_between(v1, origin)
	d2 = distance_between(v2, origin)
	d_product = d1 * d2
	dot = dot / d_product
	dot = min(1,max(dot,-1))
	acos = math.acos(dot)
	return acos * 180 / math.pi

def dot_product(v1, v2):
	return v1['x'] * v2['x'] + v1['y'] * v2['y']

def distance_between(v1, v2):
	dx = v1['x'] - v2['x']
	dy = v1['y'] - v2['y']
	return math.sqrt(dx * dx + dy * dy)
