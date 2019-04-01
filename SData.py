
import Node     # TSP Node as a class
import Problem
import mysql.connector
import wx
import datetime

class SData:

    _cnx = None

    def getConnection(self):
        cnx = mysql.connector.connect(
            user='',
            database='1810ICTdb',
            # database='s5113170db',
            host='mysql.ict.griffith.edu.au',
            password='')
        return cnx

    # List all problems
    def ListAllProblems(self):
        dat = []

        # Get Connection
        cnx = self.getConnection()

        # Build Query
        # query = """SELECT * FROM Problem"""
        query = ("SELECT * FROM Problem")

        # Perform Query
        cur = cnx.cursor(buffered=True)
        cur.execute(query)
        for c in cur:
            dat.append(c[0])

        # Housekeeping
        cur.close()
        cnx.close()

        return dat

    # List all solutions
    def ListAllSolutions(self):
        dat = []

        # Get Connection
        cnx = self.getConnection()

        # Build Query
        # query = """SELECT * FROM Problem"""
        query = ("SELECT * FROM Solution")

        # Perform Query
        cur = cnx.cursor(buffered=True)
        cur.execute(query)
        for c in cur:
            dat.append(c[1])

        # Housekeeping
        cur.close()
        cnx.close()

        return dat

    # Add Problem to database
    def AddProblem(self, Problem):
        # Get Connection
        cnx = self.getConnection()

        # Build Problem Query
        query = ("INSERT INTO Problem "
                 "(Name, Comment) "
                 "VALUES (%s, %s)")
        values = (Problem.getName(), Problem.getDescription())

        # Perform Problem Query
        cur = cnx.cursor(buffered=True)
        try:
            cur.execute(query, values)
            cnx.commit()
        except mysql.connector.errors.DatabaseError as e:
            wx.MessageBox("Database Error: " + Problem.getName() + " already exists in database")
            cur.close()
            cnx.close()
            return

        # Build Cities Query
        query = ("INSERT INTO Cities "
                 "(ID, Name, X, Y)"
                 "VALUES (%s, %s, %s, %s)")

        # Get Nodes for Problem
        nodes = Problem.getNodes()
        name = Problem.getName()

        # Perform Insert for each node into Cities
        for node in nodes:
            nid = str(node.getid())
            x = str(node.getx())
            y = str(node.gety())
            values = (nid, name, x, y)
            cur.execute(query, values)
        cnx.commit()

        # Housekeeping
        cur.close()
        cnx.close()

    # Add a solution to the database
    def AddSolution(self, problem):
        # Get Connection
        cnx = self.getConnection()
        name = problem.getName()
        query = ('SELECT * FROM Solution WHERE ProblemName = "' + name + '"')
        # Perform Solution Query
        cur = cnx.cursor(buffered=True)
        try:
            cur.execute(query)
            d = cur.fetchone()
            if d is not None:
                a = float(d[2])
                b = float(problem.getSolveLength())
                if a < b:
                    wx.MessageBox("Sorry but there is a shorter solution already saved in the database for "
                                  + problem.getName())
                    return
                else:
                    query = ('DELETE FROM Solution WHERE ProblemName = "' + problem.getName() + '"')
                    cur.execute(query)
                    cnx.commit()
        except mysql.connector.errors.DatabaseError as e:
            wx.MessageBox("Database Error: " + problem.getName() + " already exists in database")
            cur.close()
            cnx.close()
            return
        finally:
            cnx.commit()

        # Get Date in format for SQL
        now = datetime.datetime.now().strftime('%Y-%m-%d')

        # Build Tour String
        tour = ''
        for n in problem.getNodes():
            tour = tour + n.getid() + ' '
        tour = tour + '-1'

        # Build Solution Query
        query = ("INSERT INTO Solution "
                 "(ProblemName, TourLength, Date, Author, Algorithm, RunningTime, Tour) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        values = (problem.getName(),
                  problem.getSolveLength(),
                  now,
                  problem.getAuthor(),
                  problem.getAlgorithm(),
                  problem.getSolveTime(),
                  tour)

        # Perform Solution Query
        cur = cnx.cursor(buffered=True)
        try:
            cur.execute(query, values)
        except mysql.connector.errors.DatabaseError as e:
            wx.MessageBox("Database Error: " + problem.getName() + " already exists in database")
            cur.close()
            cnx.close()
            return
        finally:
            cnx.commit()

        # Housekeeping
        cur.close()
        cnx.close()

    # Open a Problem
    def OpenProblem(self, problemName):
        # Get Connection
        cnx = self.getConnection()

        p = Problem.Problem()

        # Build Query
        query = ('SELECT * FROM Problem '
                 'WHERE Name = "' + problemName + '"')

        data = ''
        # Perform Query
        cur = cnx.cursor()
        try:
            cur.execute(query)
            data = cur.fetchone()
        except mysql.connector.errors.DatabaseError as e:
            wx.MessageBox("Database Error: " + problemName + " not found in database")
            cur.close()
            cnx.close()
            return

        p.setName(data[0])
        p.setDescription(data[2])

        # Build Query
        query = ('SELECT * FROM Cities '
                 'WHERE Name = "' + problemName + '"')

        try:
            cur.execute(query)
            data = cur.fetchall()
        except mysql.connector.errors.DatabaseError as e:
            wx.MessageBox("Database Error: " + problemName + " not found in database")
            cur.close()
            cnx.close()
            return

        # Housekeeping
        cur.close()
        cnx.close()

        for d in data:
            p.addNode(str(d[1]), float(d[2]), float(d[3]))

        return p

    # Open a Problem
    def OpenSolution(self, name):
        # Get Connection
        cnx = self.getConnection()

        s = Problem.Problem()

        # Build Query
        query = ('SELECT * FROM Solution '
                 'WHERE ProblemName = "' + name + '"')

        data = ''

        # Perform Query
        cur = cnx.cursor()
        try:
            cur.execute(query)
            data = cur.fetchone()
            cnx.commit()
        except mysql.connector.errors.DatabaseError as e:
            wx.MessageBox("Database Error: " + name + " not found in database\n" + e.msg)
            cur.close()
            cnx.close()
            return

        s.setName(data[1])
        s.setSolveLength(data[2])
        s.setAuthor(data[4])
        s.setAlgorithm(data[5])
        s.setSolveTime(data[6])
        tour = data[7]

        # Build Query
        query = ('SELECT Comment FROM Problem '
                 'WHERE Name = "' + name + '"')

        # Perform Query
        cur = cnx.cursor()
        try:
            cur.execute(query)
            data = cur.fetchone()
        except mysql.connector.errors.DatabaseError as e:
            wx.MessageBox("Database Error: " + name + " not found in database\n" + e.msg)
            cur.close()
            cnx.close()
            return
        s.setDescription(data[0])

        # Build Query
        query = ('SELECT * FROM Cities '
                 'WHERE Name = "' + name + '"')

        try:
            cur.execute(query)
            data = cur.fetchall()
        except mysql.connector.errors.DatabaseError as e:
            wx.MessageBox("Database Error: " + name + " not found in database\n" + e.msg)
            cur.close()
            cnx.close()
            return

        # Housekeeping
        cur.close()
        cnx.close()

        for d in data:
            s.addNode(str(d[1]), float(d[2]), float(d[3]))

        s.setTourByString(tour)

        return s
