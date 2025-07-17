"""
/*******************************************************************************
 *
 *            #, #,         CCCCCC  VV    VV MM      MM RRRRRRR
 *           %  %(  #%%#   CC    CC VV    VV MMM    MMM RR    RR
 *           %    %## #    CC        V    V  MM M  M MM RR    RR
 *            ,%      %    CC        VV  VV  MM  MM  MM RRRRRR
 *            (%      %,   CC    CC   VVVV   MM      MM RR   RR
 *              #%    %*    CCCCCC     VV    MM      MM RR    RR
 *             .%    %/
 *                (%.      Computer Vision & Mixed Reality Group
 *
 ******************************************************************************/
/**          @copyright:   Hochschule RheinMain,
 *                         University of Applied Sciences
 *              @author:   Prof. Dr. Ulrich Schwanecke, Fabian Stahl
 *             @version:   2.0
 *                @date:   01.04.2023
 ******************************************************************************/
/**         bezierTemplate.py
 *
 *          Simple Python template to generate curve points based given a list
 *          of control points. Results are displayed in a 2D scene using OpenGL.
 ****
"""

import numpy as np
import copy

from rendering import Scene, RenderWindow


def determine_points_on_bezier_curve(points, curve_type):
    """Calculates curve points based on a list of control points.

    :param  str                         curve_type: The curve type, is either 'casteljau' or 'subdivide'
    :param 	List[Tuple[float, float]]   points:     A list of controll points
    :return	List[Tuple[float, float]]   points:     A list of curve points
    """

    # TODO: Implement two different algorithms to determine points on a bezier curve
    #   1. Implementing de Casteljaus algorithm
    #   2. Implementing repeated subdivision

    return [p + 50 * (np.random.random(2) - .5) for p in points]

def get_points_on_bspline_curve(control_points, curve_type='deboor'):
    degree = 3  # Beispielhaft Grad 3 (Kubisch)
    if len(control_points) < degree + 1:
        return control_points

    n = len(control_points)
    # Uniformer Knotenvektor mit clamped ends
    knot_vector = [0]*degree + list(range(n - degree + 1)) + [n - degree]*degree
    knot_vector = [float(u) for u in knot_vector]

    # Parameterbereich [u_k, u_{n+1}]
    t_min = knot_vector[degree]
    t_max = knot_vector[-degree-1]

    num_curve_points = 100
    ts = np.linspace(t_min, t_max, num_curve_points)

    curve_points = [deboor(degree, control_points, knot_vector, t) for t in ts]
    return curve_points


def deboor(degree, control_points, knot_vector, t):
    """
    Calculates a point on a B-Spline curve using the Deboor algorithm.

    :param degree: polynom degree of the curve (e.g. 3 for cubic)
    :param control_points: list of control points [(x0,y0),(x1,y1),...]
    :param knot_vector: list of knot vectors [u0, u1, ..., um]
    :param t: param value, at which the point on the curve should be calculated
    :return: point (x,y) on a B-Spline curve
    """

    k = degree
    n = len(control_points) - 1

    # Find the interval for t
    for i in range(len(knot_vector) - 1):
        if knot_vector[i] <= t < knot_vector[i + 1]:
            break
        else:
            # Special case: t == last knot value
            i = len(knot_vector) - degree - 2

    # Initialize B-Spline control points d_j = p_{i-k+j}
    d = [np.array(control_points[j]) for j in range(i-k, i+1)]

    # recursion
    for r in range(1, k + 1):
        for j in range(k, r - 1, -1):
            alpha = (t - knot_vector[i - k + j]) / (knot_vector[j + i - r + 1] - knot_vector[i - k + j])
            d[j] = (1.0 - alpha) * d[j - 1] + alpha * d[j]

    return d[k]

# call main
if __name__ == '__main__':
    print("bezierTemplate.py")
    print("pressing 'C' should clear the everything")

    # set size of render viewport
    width, height = 640, 480

    # instantiate a scene
    scene = Scene(width, height, get_points_on_bspline_curve, "B-Spline Curve by Porsche®")

    rw = RenderWindow(scene)
    rw.run()
