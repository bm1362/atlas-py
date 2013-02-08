"""
geometry.py: A collection of functions to aid in the movement of our entities.
"""

def is_in_polygon(vertices, point):
    x_min = vertices[0][0]
    x_max = vertices[0][0]
    y_min = vertices[0][1]
    y_max = vertices[0][1]
    sides = []

    # get max and mins
    for _ in vertices:
        if x_min > _[0]:
            x_min = _[0]

        if x_max < _[0]:
            x_max = _[0]

        if y_min > _[1]:
            y_min = _[1]
        
        if y_max < _[1]:
            y_max = _[1]

    # padding for our bounding box
    e = ((x_max - x_min) / 100) * 3 # 3 %

    if point[0] < (x_min-e) or point[0] > (x_max+e) or point[1] < (y_min-e) or point[1] > (y_max+e):
        return False
    else:
        return True

    # potentially more refined implementation
    # ray_start = (x_min - e, point[1])
    # ray_end = point

    # for i in xrange(0, len(vertices) - 1):
    #     sides.append((vertices[i], vertices[i+1]))

    # #find intersections
