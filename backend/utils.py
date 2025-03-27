import math

def calculate_polygon_area(polygon):
    """Calculate the area of a polygon using the shoelace formula."""
    n = len(polygon)
    if n < 3:
        return 0  # A polygon must have at least 3 points

    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += polygon[i][0] * polygon[j][1]
        area -= polygon[j][0] * polygon[i][1]
    area = abs(area) / 2.0
    return area

def line_intersects_circle(line_start, line_end, circle_center, circle_radius):
    """Check if a line segment intersects a circle."""
    x1, y1 = line_start
    x2, y2 = line_end
    cx, cy = circle_center

    # Check if the line segment has zero length
    if x1 == x2 and y1 == y2:
        # If the point is within the circle radius, it's a collision
        dist = math.sqrt((cx - x1) ** 2 + (cy - y1) ** 2)
        return dist <= circle_radius

    # Vector from line start to line end
    line_vec_x = x2 - x1
    line_vec_y = y2 - y1

    # Vector from line start to circle center
    circle_vec_x = cx - x1
    circle_vec_y = cy - y1

    # Calculate line length squared
    line_length_sq = line_vec_x ** 2 + line_vec_y ** 2

    # Project circle vector onto line vector
    t = max(0, min(1, (circle_vec_x * line_vec_x + circle_vec_y * line_vec_y) / line_length_sq))

    # Closest point on the line segment to the circle center
    closest_x = x1 + t * line_vec_x
    closest_y = y1 + t * line_vec_y

    # Distance between closest point and circle center
    dist_x = cx - closest_x
    dist_y = cy - closest_y

    # Check if distance is less than circle radius
    return (dist_x ** 2 + dist_y ** 2) <= circle_radius ** 2