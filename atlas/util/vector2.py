import math

# rotates a vector clockwise
def rotate_vector(vector, angle):
    x = vector['x']
    y = vector['y']
    cosa = math.cos(angle * math.pi / 180)
    sina = math.sin(angle * math.pi / 180)

    result = dict(x = x * cosa - y * sina, y = x * sina + y * cosa)
    return result

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