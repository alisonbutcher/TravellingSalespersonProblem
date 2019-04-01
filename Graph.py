import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import wx


class Graph(wx.Panel):

    canvas = None

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, size=(680, 480))

        self.figure = Figure()
        # self.axes = self.figure.add_subplot(111)

        # t = [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        # s = [0.0, 1.0, 0.0, 1.0, 0.0, 2.0, 1.0, 2.0, 1.0, 0.0]
        #
        # self.axes.plot(t, s)
        self.canvas = FigureCanvas(self, -1, self.figure)

    def plot(self, nodes):
        fig = Figure()

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
        plot = fig.add_subplot(111)
        plot.plot(y, x)
        self.canvas = FigureCanvas(self, -1, fig)


