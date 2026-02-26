# Thanks Gemini 3
import numpy as np
from fontTools.ttLib import TTFont
from fontTools.pens.basePen import BasePen

class PointExtractorPen(BasePen):
    def __init__(self, glyphset, origin=(0, 0), size=1):
        super().__init__(glyphset)
        self.ox, self.oy = origin
        self.points = []
        self.size = size

    def _add_pt(self, x, y):
        self.points.append((x*self.size + self.ox, y*self.size + self.oy))

    def _moveTo(self, pt):
        self._add_pt(*pt)
        self._last_pt = pt

    def _lineTo(self, pt):
        self._add_pt(*pt)
        self._last_pt = pt

    def _qCurveToOne(self, pt1, pt2):
        """
        Bounds the quadratic spline using P0, midpoints, and P2.
        P0 is the last point recorded.
        """
        p0 = self._last_pt
        # Midpoint 1: 1/2(P0 + P1)
        m1 = (0.5 * (p0[0] + pt1[0]), 0.5 * (p0[1] + pt1[1]))
        # Midpoint 2: 1/2(P1 + P2)
        m2 = (0.5 * (pt1[0] + pt2[0]), 0.5 * (pt1[1] + pt2[1]))
        
        # We add the midpoints and the end point. 
        # (P0 is already in the list from the previous command)
        self._add_pt(*m1)
        self._add_pt(*m2)
        self._add_pt(*pt2)
        self._last_pt = pt2

    def _curveToOne(self, pt1, pt2, pt3):
        """Optional: Cubic curves (if used in OTF/CFF fonts)"""
        # For cubics, you can use the same logic or just the 4 points
        self._add_pt(*pt1)
        self._add_pt(*pt2)
        self._add_pt(*pt3)
        self._last_pt = pt3

def get_convex_hull(points):
    """Monotone Chain algorithm to find the convex hull of a set of 2D points."""
    n = len(points)
    if n <= 2: return points
    
    # Sort points lexicographically (by x, then y)
    points = sorted(set(map(tuple, points)))
    
    def cross_product(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return np.array(lower[:-1] + upper[:-1])

def get_axes(poly):
    """Calculate the normal vectors (axes) for each edge of a polygon."""
    axes = []
    for i in range(len(poly)):
        p1 = poly[i]
        p2 = poly[(i + 1) % len(poly)]
        edge = p2 - p1
        # Get the normal (perpendicular) vector: (-y, x)
        normal = np.array([-edge[1], edge[0]])
        # Normalize
        norm = np.linalg.norm(normal)
        if norm != 0:
            axes.append(normal / norm)
    return axes

def project(poly, axis):
    """Project a polygon onto a specific axis."""
    dots = [np.dot(p, axis) for p in poly]
    return min(dots), max(dots)

def hulls_collide(poly1, poly2, t):
    """Separating Axis Theorem (SAT) to detect collision between two convex polygons."""
    # Check axes from both polygons
    if not len(poly1) or not len(poly2):
        return False
    axes = get_axes(poly1) + get_axes(poly2)
    
    for axis in axes:
        min1, max1 = project(poly1, axis)
        min2, max2 = project(poly2, axis)
        
        # If there is a gap, they do not collide
        if max1 + t < min2 or max2 + t < min1:
            return False
    return True

# --- Glyph Workflow ---

def get_glyph_hull(gs, glyph_name, p, s):
    pen = PointExtractorPen(gs, origin=p, size=s)
    gs[glyph_name].draw(pen)
    return get_convex_hull(pen.points)

def glyph_collision(font1, font2, gid1, gid2, p1, p2, s1, s2, threshold):
    gn1 = font1.getGlyphName(gid1)
    gn2 = font2.getGlyphName(gid2)
    gs1 = font1.getGlyphSet()
    gs2 = font2.getGlyphSet()
    hull1 = get_glyph_hull(gs1, gn1, p1, s1)
    hull2 = get_glyph_hull(gs2, gn2, p2, s2)
    return hulls_collide(hull1, hull2, threshold)

# Example Usage:
# hull_A = get_glyph_hull("myfont.ttf", "A")
# hull_B = get_glyph_hull("myfont.ttf", "B")
# collision = hulls_collide(hull_A, hull_B)
