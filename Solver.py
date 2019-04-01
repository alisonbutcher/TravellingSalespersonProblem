import math
import time
import matplotlib.pyplot as plt
import Node     # TSP Node as a class
import Problem  # TSP Problem Metadata

class Solver:
    # Parse input file
    def getTSPfromFile(self, filename):
        try:
            fh = open(filename, mode='r')
        except IOError:
            print("File " + filename + " does not exist, exiting.")
            exit(0)
        ncs = False  # in node_coord_section of file
        problem = Problem.Problem()
        problem.setFilename(filename)
        for line in fh:
            if line.startswith("NODE_COORD_SECTION\n"):
                # Set flag for node coord data follows
                ncs = True
            elif line.startswith("NAME"):
                n = line.rsplit(":")
                name = str(n[1]).strip()
                problem.setName(name)
            elif line.startswith("COMMENT"):
                l = line.rsplit(":")
                desc = str(l[1]).strip()
                problem.setDescription(desc)
            elif line.startswith("EOF\n"):
                ncs = False
            elif ncs:
                # parse coordinates
                node = line.split()
                obj = Node.TSPNode(node[0], node[1], node[2])
                problem.addNodeObj(obj)

        fh.close()
        return problem

    # Optimisation Loop (for either 2 or 3 opt)
    def optLoop(self, nodes, maxtime):
        endtime = time.time() + maxtime

        n = nodes   # duplicate list (non destructive)

        shorter = True      # Loop until no better route found

        bdist = self.getTourLength(n)       # Best Distance

        # number of nodes in tour
        size = len(n) - 1

        while shorter:

            # If loop gets above maxtime quit
            if time.time() > endtime:
                print("Maximum Timeout of", maxtime, "seconds has been reached. Ending with the data we have so far...")
                return n

            # start looking for better routes
            shorter = False
            for outer in range(size):
                for inner in range(outer + 1, size + 1):

                    # swap routine
                    newtour = []
                    newtour.extend(n[0:outer])  # Get section before sublist to be reversed
                    newtour.extend(list(reversed(n[outer:inner + 1])))  # Get section to be reversed and reverse it
                    newtour.extend(n[inner + 1:])  #

                    # TODO: just measure section that was changed, not the whole list

                    newdist = self.getTourLength(newtour)
                    if newdist < bdist:
                        shorter = True
                        bdist = newdist
                        n.clear()
                        n = newtour
                        break
                if shorter:
                    break
        return n

    # Calculate Tour Length
    def getTourLength(self, nodes):

        tlength = 0

        # process tour
        for idx, node in enumerate(nodes):
            # Check for last index
            if idx == (len(nodes) - 1):
                # Last node points to first
                n2 = nodes[0]
            else:
                n2 = nodes[idx + 1]

            # Get current edge length
            tlength = tlength + self.getEdgeLength(node, n2)
        return round(tlength, 1)

    # Get Distance between two nodes from nodeid
    def getEdgeLength(self, node1, node2):
        a = abs(float(node1.getx()) - float(node2.getx()))
        b = abs(float(node1.gety()) - float(node2.gety()))
        return round(math.hypot(a, b), 6)

    # Nearest Neighbour solver
    def greedySolver(self, nodes):
        newtour = []
        count = len(nodes)

        # Start with first node (pop also removes it from the tour)
        newtour.append(nodes.pop(0))

        loop = True

        # outer loop
        while loop:

            # Reset minimum distance variables
            sdist = 9999999999999999.99  # Shortest Distance
            snode = None  # Closest Node
            sindex = -1

            # Get the last item in the new tour
            node = newtour[-1]

            nid = node.getid()

            for i2, n2 in enumerate(nodes):

                # not the same node and not already processed
                if nid != n2.getid():  # and not n2.getmatch():

                    # Perform distance calculation
                    dist = self.getEdgeLength(node, n2)

                    # Is it a better route
                    if dist < sdist:
                        sdist = dist
                        sindex = i2  # TODO: find the element at current index
                        snode = n2

            # better route found
            if sindex != -1:
                # Add shortest node to the new list
                newtour.append(snode)  # add matched node to new list
                del nodes[sindex]  # remove matched node from original list

            # If Tour processed end while loop
            count = count - 1
            if count <= 0:
                loop = False

        return newtour

    def Graph(self, nodes):

        x = []
        y = []
        for n in nodes:
            x1 = float(n.getx())
            y1 = float(n.gety())
            x.append(x1)
            y.append(y1)

        x2 = float(nodes[0].getx())
        y2 = float(nodes[0].gety())
        x.append(x2)
        y.append(y2)
        plt.plot(x, y)
        plt.show()

    def Solve(self, problem, maxtime):
        if problem is not -1:

            # Run greedy solver
            nodes = problem.getNodes()
            problem.replaceAllNodes(self.greedySolver(nodes))

            # Run 2opt Solver
            t = time.time()
            problem.replaceAllNodes(self.optLoop(problem.getNodes(), int(maxtime)))
            problem.setSolveTime(round(time.time() - t, 0))

            # Calculate Tour Length ater solving
            problem.setSolveLength(self.getTourLength(problem.getNodes()))

            # Build Tour String
            tour = ''
            for n in problem.getNodes():
                tour = tour + n.getid() + ' '
            tour = tour + '-1'
            problem.setTourByString(tour)

            # Graph(pr.getNodes())
        else:
            print("Sorry I cant find a problem named xxx in the database")
        return problem
