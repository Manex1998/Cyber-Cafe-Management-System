from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        # Central widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main Layout
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Navigation Buttons (Top)
        self.navBar = QtWidgets.QHBoxLayout()
        self.navButtons = {}
        for name in ["Workstations", "Cards", "Clients", "Services", "Session Journal", "Income Journal"]:
            btn = QtWidgets.QPushButton(name)
            btn.setObjectName(name.lower().replace(" ", "_"))
            btn.clicked.connect(lambda _, n=name: self.switch_page(n))
            self.navButtons[name] = btn
            self.navBar.addWidget(btn)
        self.mainLayout.addLayout(self.navBar)

        # Splitter Layout (Main Area)
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        # Left Panel
        self.leftPanel = QtWidgets.QWidget()
        self.leftLayout = QtWidgets.QVBoxLayout(self.leftPanel)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)

        # Console Button
        self.consoleButton = QtWidgets.QPushButton("Console")
        self.consoleButton.setObjectName("consoleButton")
        self.consoleButton.setFixedWidth(150)
        self.consoleButton.clicked.connect(self.show_console)
        self.leftLayout.addWidget(self.consoleButton)

        # Scroll Area
        self.scrollArea = QtWidgets.QScrollArea(self.leftPanel)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        # Scroll Area Content
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        # Example PCs in QListWidget
        self.pcList = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.pcList.addItems([f"PC {i + 1}" for i in range(20)])
        self.scrollLayout.addWidget(self.pcList)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.leftLayout.addWidget(self.scrollArea)

        self.splitter.addWidget(self.leftPanel)

        # Right Panel (Dynamic Content)
        self.rightPanel = QtWidgets.QStackedWidget()
        self.rightPanel.setObjectName("rightPanel")

        # Add placeholder pages for navigation
        for name in ["Workstations", "Cards", "Clients", "Services", "Session Journal", "Income Journal"]:
            page = QtWidgets.QLabel(f"{name} Content")
            page.setAlignment(QtCore.Qt.AlignCenter)
            self.rightPanel.addWidget(page)

        # Console Page
        self.consolePage = QtWidgets.QTextEdit()
        self.consolePage.setObjectName("consolePage")
        self.consolePage.setText("Console Output Here...")
        self.rightPanel.addWidget(self.consolePage)

        self.splitter.addWidget(self.rightPanel)

        self.mainLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu Bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)

        # Status Bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        # Menus
        self.menuFile = QtWidgets.QMenu(self.menubar, title="File")
        self.menuMode = QtWidgets.QMenu(self.menubar, title="Mode")
        self.menuTools = QtWidgets.QMenu(self.menubar, title="Tools")
        self.menuHelp = QtWidgets.QMenu(self.menubar, title="Help")

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuMode.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        # Default Page
        self.switch_page("Workstations")

    def switch_page(self, page_name):
        """Switch to the page corresponding to the button clicked."""
        for i in range(self.rightPanel.count() - 1):  # Exclude console page
            if self.rightPanel.widget(i).text() == f"{page_name} Content":
                self.rightPanel.setCurrentIndex(i)
                break

    def show_console(self):
        """Show the console in the right panel."""
        self.rightPanel.setCurrentWidget(self.consolePage)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
