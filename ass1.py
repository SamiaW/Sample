#!/usr/bin/env python
from  __future__ import division
import sys
import re
from ast import literal_eval
import math


listOfStreets=[]
allLines = []
vertices = []
V = {}
edges = []
rawEdges=[]
pointOfInterSections = []
poiIndex = []
poiByList = []
blackListEdges = []
refinedEdges = []
E = []


class Point(object):
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'


class Line(object):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
    def __str__(self):
        return str(self.src) + '-->' +str(self.dst)


def intersect(l1, l2):
    x1,y1 = l1.src[0], l1.src[1]
    x2,y2 = l1.dst[0], l1.dst[1]
    x3,y3 = l2.src[0], l2.src[1]
    x4, y4 = l2.dst[0], l2.dst[1]

    xnum = ((x1*y2-y1*x2) * (x3-x4) - (x1-x2) * (x3*y4-y3*x4))
    xden = ((x1-x2) * (y3-y4) - (y1-y2) * (x3-x4))
    if xden != 0:
        xcoor = xnum / xden
    else:
        return 'Error, divide by zero, slope might be same.'

    ynum = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4))
    yden = ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    if xden != 0:
        ycoor = ynum / yden
    else:
        return 'Error, divide by zero, slope might be same.'

    return (xcoor,ycoor)


def is_lines_equal (l1,l2):
    if (l1.src == l2.src) and (l1.dst == l2.dst):
        return True
    else:
        return False


def in_domain_and_range(d1,r1,d2,r2,intersection):
    if (intersection[0] >= d1[0]) and (intersection[0] >= d2[0]):
        if (intersection[0] <= d1[1]) and (intersection[0] <= d2[1]):
            if (intersection[1] >= r1[0]) and (intersection[1] >= r2[0]):
                if (intersection[1] <= r1[1]) and (intersection[1] <= r2[1]):
                    return True
    else:
        return False


def all_intersections_with_line(l1):
    for i in range(len(allLines)):
        testLine = allLines[i]
        if is_lines_equal(l1, testLine):
            pass
        else:
            intersection = intersect(l1,testLine)
            if (type(intersection) is not str):
                potentialSamePoints = False
                if (l1.src == testLine.src) or (l1.dst == testLine.dst) or (l1.src == testLine.dst) or (l1.dst == testLine.src):
                    potentialSamePoints = True

                if (not potentialSamePoints):

                    d1 = sorted((l1.src[0], l1.dst[0]))  # X values of src and dst
                    r1 = sorted((l1.src[1], l1.dst[1]))  # Y values of src and dst

                    d2 = sorted((testLine.src[0], testLine.dst[0]))  # X values of src and dst
                    r2 = sorted((testLine.src[1], testLine.dst[1]))  # Y values of src and dst

                    if in_domain_and_range(d1,r1,d2,r2,intersection):
                        makeEdges(l1.src, l1.dst ,testLine.src ,testLine.dst ,intersection)
                        if intersection not in vertices:
                            vertices.append(intersection)
                            pointOfInterSections.append(intersection)
                        if l1.src not in vertices:
                            vertices.append(l1.src)
                        if l1.dst not in vertices:
                            vertices.append(l1.dst)
                        if testLine.src not in vertices:
                            vertices.append(testLine.src)
                        if testLine.dst not in vertices:
                            vertices.append(testLine.dst)

            if (type(intersection) is str):
                d1 = sorted((l1.src[0], l1.dst[0]))  # X values of src and dst
                r1 = sorted((l1.src[1], l1.dst[1]))  # Y values of src and dst

                d2 = sorted((testLine.src[0], testLine.dst[0]))  # X values of src and dst
                r2 = sorted((testLine.src[1], testLine.dst[1]))  # Y values of src and dst

                if ((r1[1] <= r2[0]) and (d2[0] <= d1[1])):
                    makeEdgesSameSlope(l1.src, l1.dst, testLine.src, testLine.dst)
                    if l1.src not in vertices:
                        vertices.append(l1.src)
                    if l1.dst not in vertices:
                        vertices.append(l1.dst)
                        pointOfInterSections.append(l1.dst) ##########
                    if testLine.src not in vertices:
                        vertices.append(testLine.src)
                        pointOfInterSections.append(testLine.src) #########a
                    if testLine.dst not in vertices:
                        vertices.append(testLine.dst)

                elif ((r2[1] <= r1[0]) and (d1[0] <= d2[1])):
                    makeEdgesSameSlope(testLine.src, testLine.dst, l1.src, l1.dst)
                    if l1.src not in vertices:
                        vertices.append(l1.src)
                        pointOfInterSections.append(l1.src)
                    if l1.dst not in vertices:
                        vertices.append(l1.dst)
                    if testLine.src not in vertices:
                        vertices.append(testLine.src)
                    if testLine.dst not in vertices:
                        vertices.append(testLine.dst)
                        pointOfInterSections.append(testLine.dst) ############



def makeEdges(l1src,l1dst,l2src,l2dst,intersection):
    edge1 = (l1src,intersection)
    edge2 = (l1dst, intersection)
    edge3 = (l2src, intersection)
    edge4 = (l2dst, intersection)

    if edge1 not in rawEdges:
        rawEdges.append(edge1)
    if edge2 not in rawEdges:
        rawEdges.append(edge2)
    if edge3 not in rawEdges:
        rawEdges.append(edge3)
    if edge4 not in rawEdges:
        rawEdges.append(edge4)

def makeEdgesSameSlope(l1src,l1dst,l2src,l2dst):
    edge1 = (l1src, l2src)
    edge2 = (l2src, l1dst)
    edge3 = (l1dst, l2dst)

    if edge1 not in rawEdges:
        rawEdges.append(edge1)
    if edge2 not in rawEdges:
        rawEdges.append(edge2)
    if edge3 not in rawEdges:
        rawEdges.append(edge3)


def getStreetNameAndCoords(line):
    import re
    from ast import literal_eval

    splitLine = line.split("\"")

    streetName = splitLine[1]

    coordRegex = re.compile(r'\s*\(\s*(-)?[0-9]+\s*,\s*(-)?[0-9]+\s*\)(\s*\(\s*(-)?[0-9]+\s*,\s*(-)?[0-9]+\s*\)\s*)+')
    mo = coordRegex.search(splitLine[2])

    coordsInString = mo.group()

    coordsInString = coordsInString.rstrip('\n')

    coordsInString = coordsInString.replace(" ", "")

    for i in range(1, len(coordsInString)):
        try:
            if coordsInString[i - 1] == ')' and coordsInString[i] == '(':
                coordsInString = coordsInString[:i] + ' ' + coordsInString[i:]
        except:
            pass

    coords = coordsInString.split(" ")

    for i in range(len(coords)):
        coords[i] = literal_eval(coords[i])

    coords = tuple(coords)

    return streetName,coords


def makeAllLinesOnce(coords):
    #((2,1), (2,2))
    lines = []
    for i in range(len(coords) - 1):
        line = Line(coords[i], coords[i+1])
        lines.append(line)
        allLines.append(line) #Global variable to keep track of all possible lines.
    return lines


def updateGlobalAllLines():
    global allLines
    allLines = []

    for i in range (len(listOfStreets)):
        coords = listOfStreets[i]['Coordinates']
        for i in range (len(coords) -1):
            line = Line(coords[i],coords[i+1])
            allLines.append(line)


def makeVerticesDictionary(vertices):
    v = {}
    for i in range (len(vertices)):
        v[i+1] = vertices[i]
    return v


def a(s):
    #Get street Name and coords
    streetName, streetCoords= getStreetNameAndCoords(s)

    streets = {}
    streets['Name'] = streetName
    streets['Coordinates'] = streetCoords
    streetLines = makeAllLinesOnce(streetCoords)
    streets['Lines'] = streetLines
    listOfStreets.append(streets)


def c(s):
    streetName, streetCoords = getStreetNameAndCoords(s)

    exists = False

    for i in range (len(listOfStreets)):
        name = listOfStreets[i]['Name']
        if name.lower() == streetName.lower():
            exists = True
            listOfStreets[i]['Coordinates'] = streetCoords
            streetLines = makeAllLinesOnce(streetCoords)
            listOfStreets[i]['Lines'] = streetLines
            updateGlobalAllLines()
            break

    if exists == False:
        raise Exception('Error: c specified for a street that does not exist.')


def r(sname):
    sname = sname.rstrip('\n')
    try:
        indexOfFirstQuotationMark = sname.index("\"")
    except:
        raise ('Error: Imporper format.')
    sname = sname[indexOfFirstQuotationMark:]
    sname = sname[1:]
    sname = sname[:-1]

    exists = False

    for i in range (len(listOfStreets)):
        name = listOfStreets[i]['Name']
        name = (name).lower()

        if sname.lower() == name:
            exists = True
            listOfStreets.pop(i)
            updateGlobalAllLines()
            break
    if exists == False:
        raise Exception('Error: r specified for a street that does not exist.')


def g():

    global vertices
    vertices = []

    global edges
    edges = []

    global rawEdges
    rawEdges = []

    global pointOfInterSections
    pointOfInterSections = []

    global poiIndex
    poiIndex = []

    global poiByList
    poiByList = []

    global blackListEdges
    blackListEdges = []

    global refinedEdges
    refinedEdges = []


    for i in range(len(allLines)):
        all_intersections_with_line(allLines[i])

        global V
        V = {}
        V = makeVerticesDictionary(vertices)

        for i in range (len(pointOfInterSections)):
            for index,coord in V.iteritems():
                if coord == pointOfInterSections[i]:
                    if index not in poiIndex:
                        poiIndex.append(index)


        for i in range (len(rawEdges)):
            firstValue = rawEdges[i][0]
            firstIndex = 0
            secondValue = rawEdges[i][1]
            secondIndex = 0

            for index,coord in V.iteritems():
                if coord == firstValue:
                    firstIndex = index
                if coord == secondValue:
                    secondIndex = index


            if firstValue in (poiIndex):
                validIndex = (firstIndex, secondIndex)
                if validIndex not in edges:
                    edges.append(validIndex)
            elif secondIndex in (poiIndex):
                validIndex = (secondIndex, firstIndex)
                if validIndex not in edges:
                    edges.append(validIndex)

    makeListOfPOI(edges)

    for i in range (len(poiByList)):
        for x in range (len (poiByList[i])):
            target = poiByList[i][x]
            targetSecondInt = poiByList[i][x][1]
            for j in range (len (poiByList)):
                for k in range (len (poiByList[j])):
                    if j == i:
                        pass
                    else:
                        coTarget = poiByList[j][k]
                        coTargetSecondInt = poiByList[j][k][1]

                        if targetSecondInt == coTargetSecondInt:
                            if makeSlope(target) == makeSlope(coTarget):

                                if getDistance(target) < getDistance(coTarget):
                                    if coTarget not in blackListEdges:
                                        blackListEdges.append(coTarget)

                                    coTarget = (coTarget[0], target[0])
                                    if coTarget not in edges:
                                        edges.append(coTarget)

                                elif getDistance(target) > getDistance(coTarget):
                                    if target not in blackListEdges:
                                        blackListEdges.append(target)

                                    target = (target[0],coTarget[0])
                                    if target not in edges:
                                        edges.append(target)
    global E
    E = []
    E = makeRefinedEdges()
    displayAsA3Requirement()

def makeRefinedEdges():
    #Sort edges with lower value first
    for i in range (len (edges)):
        if (edges[i][0] > edges[i][1]):
            edges[i] = (edges[i][1], edges[i][0])

    for i in range (len (blackListEdges)):
        if (blackListEdges[i][0] > blackListEdges[i][1]):
            blackListEdges[i] = (blackListEdges[i][1], blackListEdges[i][0])

    setOfEdges = set(edges)
    setOfEdges = list(setOfEdges)
    refinedListOfEdges = list(set(setOfEdges) - set(blackListEdges))

    return refinedListOfEdges


def makeSlope(one):
    coord1,coord2 = one[0],one[1]

    x1value,x2value,y1value,y2value = 0,0,0,0

    for index,value in V.iteritems():
        if coord1 == index:
            x1value = value[0]
            y1value = value[1]
    for index,value in V.iteritems():
        if coord2 == index:
            x2value = value[0]
            y2value = value[1]


    if x2value-x1value == 0:
        slope = 'undefined'
        return 'undefined'
    else:
        slope = (y2value-y1value) / (x2value - x1value)
        return slope

def getDistance(edge):
    coord1, coord2 = edge[0], edge[1]

    x1value, x2value, y1value, y2value = 0, 0, 0, 0

    for index, value in V.iteritems():
        if coord1 == index:
            x1value = value[0]
            y1value = value[1]
    for index, value in V.iteritems():
        if coord2 == index:
            x2value = value[0]
            y2value = value[1]

    d = math.sqrt((math.pow((x2value-x1value),2) + (math.pow((y2value-y1value),2))))
    return d


def makeListOfPOI(edges):
   for i in poiIndex:
        sublist = []
        for x in range (len (edges)):

            if edges[x][0] == i and ((edges[x][0],edges[x][1]) not in sublist):
                sublist.append((edges[x][0],edges[x][1]))

        poiByList.append(sublist)


def displayVertices():
    print ("V = {")
    for key,value in V.iteritems():
        if key < len(V):
            print('  ' + str(key) + ':  ' + '(' + "{0:.2f}".format(value[0]) + ',' + "{0:.2f}".format(value[1]) + ')')
        else:
            print(
            '  ' + str(key) + ':  ' + '(' + "{0:.2f}".format(value[0]) + ',' + "{0:.2f}".format(value[1]) + ')')
    print("}")


def displayAsA3Requirement():
    print("V " + str(len(V)))
    edgesOutput = "E {"
    lengthOfE = len(E)
    i = 1
    for value in E:
        if i < lengthOfE:
            edgesOutput += '<' + str(value[0]) + ',' + str(value[1]) + '>' +','
        else:
            edgesOutput += '<' + str(value[0]) + ',' + str(value[1]) + '>'
        i+=1
    edgesOutput += "}"
    print(edgesOutput)





def displayEdges():
    print ("E = {")
    lengthOfE = len(E)
    i = 1
    for value in E:
        if i < lengthOfE:
            print('  ' + '<' + str(value[0]) + ',' + str(value[1]) + '>' + ',')
        else:
            print('  ' + '<' + str(value[0]) + ',' + str(value[1]) + '>')
        i+=1
    print("}")


def checkValidLine(letter,line):
        if letter == 'a':
            addingRegex = re.compile(
                r'a\s*\"[a-zA-Z0-9 ]+\"\s*\(\s*(-)?[0-9]+\s*,\s*(-)?[0-9]+\s*\)(\s*\(\s*(-)?[0-9]+\s*,\s*(-)?[0-9]+\s*\)\s*)+')
            mo = addingRegex.search(line)
            if mo is None:
                raise Exception('Error: Invalid input for command a')
            else:
                if mo.group() == line:
                    return True
                else:
                    return False
        elif letter == 'c':
            changingRegex = re.compile(
                r'c\s*\"[a-zA-Z0-9 ]+\"\s*\(\s*(-)?[0-9]+\s*,\s*(-)?[0-9]+\s*\)(\s*\(\s*(-)?[0-9]+\s*,\s*(-)?[0-9]+\s*\)\s*)+')
            mo = changingRegex.search(line)
            if mo is None:
                raise Exception('Error: Invalid input for command c')
            else:
                if mo.group() == line:
                    return True
                else:
                    return False
        elif letter == 'r':
            removingRegex = re.compile(r'r\s*\"[a-zA-Z0-9 ]+\"')
            mo = removingRegex.search(line)
            if mo is None:
                raise Exception('Error: Invalid input for command r')
            else:
                if mo.group() == line.rstrip('\n'):
                    return True
                else:
                    return False
        else:
            return False



def parse_line(line):
    sp = line.strip().split()

    if len(sp) == 0:
        raise Exception('Error:n0. 1  too few arguments')


    if ((len(listOfStreets)) == 0) and (line[0] != 'a'):
        raise Exception('Error: You need to add streets first.')
    elif sp[0] == 'a':
        if (not checkValidLine(sp[0],line)):
            raise Exception('Error: Invalid input for a')
    elif sp[0] == 'c':
        if (not checkValidLine(sp[0],line)):
            raise Exception('Error: Invalid input for c')
    elif sp[0] == 'r':
        if (not checkValidLine(sp[0],line)):
            raise Exception('Error: Invalid input for r')
    elif sp[0] == 'g':
        if len(sp) != 1:
            raise Exception('Error: command g can only accept one argument')
    else:
        raise Exception('Error: no. 2 unknown command')



def main():

    while True:
        line = sys.stdin.readline()

        if line == '':
            break

        try:
            parse_line(line)

            if (len(listOfStreets)) == 0:
                if line[0] == 'a' and line[1] == ' ':
                    a(line)
            else:
                if line[0] == 'a' and line[1] == ' ':
                    a(line)
                elif line[0] == 'c' and line[1] == ' ':
                    c(line)
                ## The following will not work right now.
                elif line[0] == 'r' and line[1] == ' ':
                    r(line)
                elif line[0] == 'g':
                    g()
                else:
                    raise Exception('Error: no. 3 Unknown Command')

        except Exception as ex:
            sys.stderr.write(str(ex) + '\n')

    #return exit code 0 on successful termination
    sys.exit(0)

if __name__=='__main__':
    main()























