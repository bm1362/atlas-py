"""
Geometry.py: A collection of functions to aid in the movement of our entities.
"""

def is_in_polygon(vertices, point):
    """
    Given a list of vertices and a point, returns whether or not the point is within the polygon generated by the vertices. Currently uses a bounding box approach and accepts Vector2 vertices.
    """
    x_min = min(v.x for v in vertices)
    y_min = min(v.y for v in vertices)
    x_max = max(v.x for v in vertices)
    y_max = max(v.y for v in vertices)

    # padding for our bounding box
    padding = ((x_max - x_min) / 100) * 3 # 3 %

    is_not_inside = point.x < (x_min-padding) 
    is_not_inside = is_not_inside or point.x > (x_max+padding)
    is_not_inside = is_not_inside or point.y < (y_min-padding)
    is_not_inside = is_not_inside or point.y > (y_max+padding)

    return is_not_inside == False

def project_polygon(vertices, axis):
    """
    Projects a polygon onto a axis and returns the min, max positions.

    Parameters:
        Vertices - a list of Vector2 objects
        Axis - a Vector2 representing a axis to project against
    """
    
    projections = map(lambda v: v.dot_product(axis), vertices)
    return dict(min=min(projections), max=max(projections))

def get_polygon_edges(vertices):
    """
    Returns a list of edges for the polygon as a list of tuples of Vector2. Eg: [(Vector2, Vector2), (Vector2, Vector2)]
    """
    edges = []
    for i in xrange(0, len(vertices) - 1):
        edges.append(vertices[i+1].subtract(vertices[i]))

    edges.append(vertices[-1].subtract(vertices[0]))

    return edges

def get_interval_distance(line1, line2):
    """
    Returns the distance of the two line segments. A line is represented by a dict with keys min and max.
    """

    minL1 = line1['min']
    minL2 = line2['min']
    maxL1 = line1['max']
    maxL2 = line2['max']

    if minL1 < minL2:
        return minL2 - maxL1
    else:
        return minL1 - maxL2
