import wx
import Solver
import SData
import Graph


class guiApp:
    app = wx.App()
    frame = wx.Frame(None, title='TSP Application')
    pnl = wx.Panel(frame)
    gpnl = None
    data = SData.SData()

    # Fields of the TSP Data Pane
    datPrbName = None
    datPrbDesc = None
    datTime = None
    datShortest = None
    datNumPoints = None
    lstTour = None

    # Fields of the TSP Control Pane
    txtMaxTime = None
    cmbTSPPrb = None
    cmbTSPSol = None

    sol = Solver.Solver()

    gph = None

    prb = None  # Represents problem object

    def showGUI(self):
        self.frame.SetSize(1024, 768)
        self.makeMenuBar()
        self.frame.SetMenuBar(self.makeMenuBar())
        self.frame.Center()
        self.frame.Show()
        self.makeControlArea()
        self.makeDataArea()
        self.makeGraphArea()
        self.app.MainLoop()


    def makeMenuBar(self):
        mb = wx.MenuBar()
        fileMenu = wx.Menu()
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)
        mb.Append(fileMenu, "&File")
        mb.Append(helpMenu, "&Help")
        mb.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        mb.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)
        return mb


    def makeControlArea(self):
        wx.StaticBox(self.pnl, label='TSP Problems and Solutions', pos=(20, 20), size=(965, 170))
        wx.StaticText(self.pnl, label="Problem:", pos=(45, 72))
        wx.StaticText(self.pnl, label="Solution:", pos=(45, 122))

        self.cmbTSPPrb = wx.ComboBox(self.pnl, value="select one", pos=(110, 70), size=(140, -1))
        self.cmbTSPSol = wx.ComboBox(self.pnl, value="select one", pos=(110, 120), size=(140, -1))

        btnTSPPrbOpn = wx.Button(self.pnl, label='Open Problem', pos=(260, 68), size=(120, -1))
        btnTSPSolOpn = wx.Button(self.pnl, label='Open Solution', pos=(260, 118), size=(120, -1))
        wx.StaticText(self.pnl, label="Max. Time (secs):", pos=(420, 72))
        self.txtMaxTime = wx.TextCtrl(self.pnl, value="300", pos=(525, 70), size=(70, -1))
        btnSolve = wx.Button(self.pnl, label='Solve', pos=(605, 68), size=(100, -1))
        btnSaveSol = wx.Button(self.pnl, label='Save Solution', pos=(605, 118), size=(100, -1))
        btnAddTsp = wx.Button(self.pnl, label="Add New TSP", pos=(820, 68), size=(120, -1))
        btnTSPSolOpn.Bind(wx.EVT_BUTTON, self.OpenTSPSolution)
        btnTSPPrbOpn.Bind(wx.EVT_BUTTON, self.OpenTSPProblem)
        btnSolve.Bind(wx.EVT_BUTTON, self.SolveTSPProblem)
        btnAddTsp.Bind(wx.EVT_BUTTON, self.AddTSPProblem)
        btnSaveSol.Bind(wx.EVT_BUTTON, self.SaveSolution)
        # wx.StaticText(self.pnl, label="Please Note: Only the shortest solution for each problem will be stored"
        #                          "in the system", pos=(480, 122))
        self.updatePrbCombo()
        self.updateSolCombo()


    def makeDataArea(self):
        wx.StaticBox(self.pnl, label='TSP Data', pos=(685, 205), size=(300, 488))
        wx.StaticText(self.pnl, label="Name:", pos=(705, 250))
        self.datPrbName = wx.StaticText(self.pnl, label="", pos=(805, 250), size=(162, -1))
        wx.StaticText(self.pnl, label="Description:", pos=(705, 280))
        self.datPrbDesc = wx.StaticText(self.pnl, label="", pos=(805, 280), size=(162, 40))
        wx.StaticText(self.pnl, label="Num. Points:", pos=(705, 340))
        self.datNumPoints = wx.StaticText(self.pnl, label="", pos=(805, 340), size=(162, -1))
        wx.StaticText(self.pnl, label="Distance:", pos=(705, 370))
        self.datShortest = wx.StaticText(self.pnl, label="", pos=(805, 370), size=(162, -1))
        wx.StaticText(self.pnl, label="Time:", pos=(705, 400))
        self.datTime = wx.StaticText(self.pnl, label="", pos=(805, 400), size=(162, -1))
        wx.StaticText(self.pnl, label="Tour Order:", pos=(705, 440), size=(162, -1))
        self.lstTour = wx.ListBox(self.pnl, pos=(705, 460), size=(260, 215))

    def makeGraphArea(self):
        gpnl = wx.Panel(self.pnl, pos=(20, 212), size=(640, 480), style=wx.SIMPLE_BORDER)
        self.gph = Graph.Graph(gpnl)


    def OnExit(self, event):
        self.frame.Close(True)


    def OnAbout(self, event):
        wx.MessageBox("This application solves Travelling Salesperson Problems and stores them along "
                      "with their solutions in a database",
                      "About TSP Application",
                      wx.OK | wx.ICON_INFORMATION)


    def AddTSPProblem(self, event):
        with wx.FileDialog(self.frame, "Open a TSP file", wildcard="TSP files (*.tsp)|*.tsp",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # No file selected
            self.prb = self.sol.getTSPfromFile(fileDialog.GetFilename())
            self.updateTSPDataPane()
            self.data.AddProblem(self.prb)
            self.updatePrbCombo()


    def OpenTSPProblem(self, event):
        # self.prb.clear()
        self.prb = self.data.OpenProblem(self.cmbTSPPrb.GetValue())
        self.updateTSPDataPane()


    def OpenTSPSolution(self, event):
        # self.prb.clear()
        self.prb = self.data.OpenSolution(self.cmbTSPSol.GetValue())
        self.updateTSPDataPane()
        # self.gph.plot(self.prb.getNodes())


    def SolveTSPProblem(self, event):
        self.datTime.SetLabel("")
        self.datShortest.SetLabel("")
        self.prb = self.sol.Solve(self.prb, self.txtMaxTime.GetValue())
        self.updateTSPDataPane()


    def SaveSolution(self, event):
        self.data.AddSolution(self.prb)
        self.updateSolCombo()


    def updateTSPDataPane(self):
        self.datPrbName.SetLabel(self.prb.getName())
        self.datPrbDesc.SetLabel(self.prb.getDescription())
        self.datPrbDesc.Wrap(162)
        self.datNumPoints.SetLabel(str(self.prb.getNumNodes()))
        if self.prb.getSolveTime() is not None:
            self.datTime.SetLabel(str(self.prb.getSolveTime()))
        if self.prb.getSolveLength() is not None:
            self.datShortest.SetLabel(str(self.prb.getSolveLength()))
        if self.prb.getTourAsString() is not None:
            self.lstTour.Clear()
            self.lstTour.AppendItems(self.prb.getTourAsString())
        if self.prb.getNodes() is not None:
            self.gph.plot(self.prb.getNodes())

    def updatePrbCombo(self):
        self.cmbTSPPrb.Clear()
        self.cmbTSPPrb.AppendItems(self.data.ListAllProblems())
        self.cmbTSPPrb.SetValue("select one")


    def updateSolCombo(self):
        self.cmbTSPSol.Clear()
        self.cmbTSPSol.AppendItems(self.data.ListAllSolutions())
        self.cmbTSPSol.SetValue("select one")
