MAX_ITERATIONS = 15
TOLERANCE = 0.001

# https://en.wikipedia.org/wiki/B%C3%A9zier_curve
# P0(0, 0), P1(x1, y1), P2(x2, y2), P3(1, 1)
# B(t) = ((1-t)^3)*P0 + (3t(1-t)^2)*P1 + (3t^2(1-t))*P2 + t^3*P3
#      =                (3t(1-t)^2)*P1 + (3t^2(1-t))*P2 + t^3
# Returns f(t) or z(t) by given value x1, x2 or y1, y2
def calculateBezier(t, Z1, Z2):
    return 3.0*t*Z1*((1-t)**2) + 3.0*(t**2)*Z2*(1-t) + t**3

# B`(t) = (3(1-t)^2)*P1 + (6t(1-t))(P2-P1) + 3t^2(P3-P2)
# Remember that P3 is always (1, 1)
# Returns dx/dt or dy/dt by given value x1, x2 or y1, y2
def calculateSlope(t, Z1, Z2):
    Z3 = 1.0
    return 3.0*Z1*((1-t)**2) + (6.0*t*(1-t))*(Z2-Z1) + 3.0*(t**2)*(Z3-Z2)

def newtonRaphson(X_target, X_initial, X1, X2):
    for _ in range(MAX_ITERATIONS):
        slope = calculateSlope(X_initial, X1, X2)
        if(abs(slope) <= TOLERANCE):
            return X_initial
        
        X = calculateBezier(X_initial, X1, X2) - X_target
        X_initial = X_initial - X / slope

    return X_initial

def easing(X, X1, Y1, X2, Y2):
    if (X1 < 0 or X1 > 1 or X2 < 0 or X2 > 1):
        raise Exception("X Values should be in range [0, 1]")
    
    if (X1 == Y1 and X2 == Y2):  # The curve is linear
        return X
    
    # TODO: Find optimized initial value instead of hard-coded 0.5
    T = newtonRaphson(X, 0.5, X1, X2)
    return calculateBezier(T, Y1, Y2)