import Node


# Represents metadata about a TSP Problem
class Problem:
    _filename = None
    _name = None
    _description = None
    # _problemID = None       # The value assigned in the Problem table
    _solveTime = None
    _solvedLength = 19999
    _author = 'Alison Butcher'
    _algorithm = 'Greedy 2Opt'
    # _tourString = []
    _nodes = []

    def getFilename(self):
        return self._filename

    def setFilename(self, filename):
        self._filename = filename

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getDescription(self):
        return self._description

    def setDescription(self, description):
        self._description = description

    def getSolveTime(self):
        return self._solveTime

    def setSolveLength(self, solvedLength):
        self._solvedLength = solvedLength

    def getSolveLength(self):
        return self._solvedLength

    def setSolveTime(self, solveTime):
        self._solveTime = solveTime

    def addNodeObj(self, node):
        # node = Node.TSPNode(id, xpos, ypos)
        self._nodes.append(node)

    def addNode(self, id, xpos, ypos):
        n = Node.TSPNode(id, xpos, ypos)
        self._nodes.append(n)

    def getNodes(self):
        return self._nodes

    def replaceAllNodes(self, nodes):
        self._nodes.clear()
        self._nodes = nodes

    def getNumNodes(self):
        return int(len(self._nodes))

    def setAlgorithm(self, algorithm):
        self._algorithm = algorithm

    def getAlgorithm(self):
        return self._algorithm

    def setAuthor(self, author):
        self._author = author

    def getAuthor(self):
        return self._author

    def setTourByString(self, tourstring):
        temp = tourstring.rsplit(" ")
        new = []
        # for t in temp:
        #     self._tourString.append(t)
        for t in temp:
            for n in self._nodes:
                if n.getid() == t:
                    new.append(n)
        self._nodes = new

    def getTourAsString(self):
        new = []
        for n in self._nodes:
            new.append(n.getid())
        new.append('-1')
        return new

    def clear(self):
        self._solvedLength = None
        self._solveTime = None
        self._nodes.clear()
        self._filename = None
        self._name = None
        self._description = None
