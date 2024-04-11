from sympy import *

def solvepart1():
    #read in data
    data = fileRead("input.txt")
    hailstones = []
    for row in data:
        firstHalf, secondHalf = row.strip().replace(" ","").split("@")
        pos = [ int(val) for val in firstHalf.split(",") ]
        vel = [ int(val) for val in secondHalf.split(",") ]
        hailstones.append((pos,vel))
    
    #calculate intersections
    sum = 0
    minval = 200000000000000
    maxval = 400000000000000
    for i in range(len(hailstones)):
        h1 = hailstones[i]
        for j in range(i+1, len(hailstones)):
            h2 = hailstones[j]
            s1, i1 = getSlopeAndIntercept2D(h1[0],h1[1])
            s2, i2 = getSlopeAndIntercept2D(h2[0],h2[1])
            intersects, intersectPos = getIntersection2D(s1, i1, s2, i2)
            if intersects and inRange2D(intersectPos, minval, maxval) and posInFuture2D(h1[0], h1[1], intersectPos) and posInFuture2D(h2[0], h2[1], intersectPos):
                sum += 1
    print(sum)


#finds the intersection of two 2d lines, returns false if line are parallel
#input: ax + c = y for each line
def getIntersection2D(a1,c1,a2,c2):
    if a1 == a2:
        return False, (0,0)
    b1 = -1
    b2 = -1
    x = ((b1*c2)-(b2*c1))/((a1*b2)-(a2*b1))
    y = ((c1*a2)-(c2*a1))/((a1*b2)-(a2*b1))
    return True, (x,y)

#gets the slope and y intercept of a 2d line from a position and velocity
def getSlopeAndIntercept2D(pos, vel):
    slope = vel[1] / vel[0]
    intercept = pos[1] - (pos[0]*slope)
    return slope, intercept

#checks whether a 2d point is in a range in both x and y
def inRange2D(pos, least, most):
    return pos[0] >= least and pos[0] <= most and pos[1] >= least and pos[1] <= most

#calculates whether a point is before or after another point on a graph with a given velocity, in 2d
def posInFuture2D(oldPos, velocity, newPos):
    valid = True
    if (oldPos[0] > newPos[0]) == (velocity[0] > 0):
        valid = False
    if (oldPos[1] > newPos[1]) == (velocity[1] > 0):
        valid = False
    return valid

def solvepart2():
    data = fileRead("input.txt")
    hailstones = []
    for row in data[:3]:
        firstHalf, secondHalf = row.strip().replace(" ","").split("@")
        pos = [ int(val) for val in firstHalf.split(",") ]
        vel = [ int(val) for val in secondHalf.split(",") ]
        hailstones.append((pos,vel))
    
    #enter first 3 hailstones into system of equations
    rx, ry, rz, rvx, rvy, rvz = symbols("rx ry rz rvx rvy rvz")
    all_equations = []
    times = []
    index = 0
    for hail in hailstones:
        index += 1
        pos, vel = hail
        hx, hy, hz = pos
        hvx, hvy, hvz = vel
        t = Symbol("t" + str(index))
        xEq = rx - hx + rvx*t - hvx*t 
        yEq = ry - hy + rvy*t - hvy*t 
        zEq = rz - hz + rvz*t - hvz*t 
        all_equations = all_equations + [ xEq, yEq, zEq ]
        times = times + [t]
    
    #solve equation system
    answer = solve(all_equations, [ rx, ry, rz, rvx, rvy, rvz ] + times)
    print(answer)
    print(answer[0][0]+answer[0][1]+answer[0][2])

def fileRead(name):
    data = []
    f = open(name, "r")
    for line in f:
        data.append(line);
    return data

solvepart2()