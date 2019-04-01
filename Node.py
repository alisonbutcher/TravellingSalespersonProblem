# Represents a single TPS Node in a tour
class TSPNode:
    _id = -1
    _xPos = 0.0
    _yPos = 0.0
    # _ProblemID = None

    def __init__(self, id, xPos, yPos):
        self._id = id
        self._xPos = xPos
        self._yPos = yPos

    # def __init__(self, id, xPos, yPos, ProbId):
    #     self._id = id
    #     self._xPos = xPos
    #     self._yPos = yPos
    #     self._ProblemID = ProbId


    def __str__(self):
        return self._id

    def getx(self):
        return self._xPos

    def gety(self):
        return self._yPos

    def getid(self):
        return self._id

    def getProblemId(self):
        return self._ProblemID

    def setProblemId(self, ProblemId):
        self._ProblemID = ProblemId