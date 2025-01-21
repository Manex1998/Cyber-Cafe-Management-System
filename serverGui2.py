from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)

        # Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.mainLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Tab Buttons Layout
        self.tabButtonLayout = QtWidgets.QHBoxLayout()
        self.tabButtons = {}

        # Define Tab Buttons
        self.tabs = ["Workstations", "Cards", "Clients", "Services", "Session Journal", "Income Journal"]
        for tab in self.tabs:
            button = QtWidgets.QPushButton(tab)
            button.setCheckable(True)
            button.setFlat(True)
            button.clicked.connect(lambda _, t=tab: self.switch_tab(t))
            self.tabButtons[tab] = button
            self.tabButtonLayout.addWidget(button)

        # Add Tab Buttons to Main Layout
        self.mainLayout.addLayout(self.tabButtonLayout)

        # Split Left and Right Panels
        self.contentLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.contentLayout)

        # Left Panel Layout
        self.leftPanel = QtWidgets.QVBoxLayout()

        # Console Button (above the scroll area)
        self.consoleButton = QtWidgets.QPushButton("Console")
        self.consoleButton.setFixedHeight(50)
        self.consoleButton.clicked.connect(self.show_console)

        # Add dynamic left panel content
        self.leftPanelContent = QtWidgets.QStackedWidget()
        self.leftPanel.addWidget(self.leftPanelContent)
        self.contentLayout.addLayout(self.leftPanel)

        # Right Panel (Dynamic Content)
        self.rightPanel = QtWidgets.QStackedWidget()
        self.contentLayout.addWidget(self.rightPanel)

        # Scroll Area for Workstations Tab
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        self.scrollContent = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollContent)

        for i in range(20):  # Example: 20 PCs
            pcButton = QtWidgets.QPushButton(f"PC {i + 1}")
            pcButton.setFixedHeight(50)
            pcButton.clicked.connect(lambda _, i=i: self.switch_page(f"PC {i + 1}"))
            self.scrollLayout.addWidget(pcButton)

        self.scrollArea.setWidget(self.scrollContent)

        # Add a combined widget for the Workstations tab (console + scroll area)
        self.workstationsWidget = QtWidgets.QWidget()
        self.workstationsLayout = QtWidgets.QVBoxLayout(self.workstationsWidget)
        self.workstationsLayout.addWidget(self.consoleButton)
        self.workstationsLayout.addWidget(self.scrollArea)
        self.leftPanelContent.addWidget(self.workstationsWidget)

        # Add Pages for Tabs in Right Panel
        self.tabPages = {}
        for tab in self.tabs:
            page = QtWidgets.QLabel(f"{tab} Page")
            page.setAlignment(QtCore.Qt.AlignCenter)
            self.tabPages[tab] = page
            self.rightPanel.addWidget(page)

        # Add Pages for Tabs in Left Panel
        self.leftTabPages = {}
        for tab in self.tabs:
            if tab == "Workstations":
                self.leftTabPages[tab] = self.workstationsWidget  # Console + Scroll area for Workstations
            else:
                page = QtWidgets.QLabel(f"{tab} Left Content")
                page.setAlignment(QtCore.Qt.AlignCenter)
                self.leftTabPages[tab] = page
                self.leftPanelContent.addWidget(page)

        # Add Console Page
        self.consolePage = QtWidgets.QTextEdit()
        self.consolePage.setPlainText("Console Output Here...")
        self.rightPanel.addWidget(self.consolePage)

        # Add Placeholder Pages for PCs
        self.pcPages = {}
        for i in range(20):
            pcPage = QtWidgets.QLabel(f"PC {i + 1} Information")
            pcPage.setAlignment(QtCore.Qt.AlignCenter)
            self.pcPages[f"PC {i + 1}"] = pcPage
            self.rightPanel.addWidget(pcPage)

        # Menu Bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)

        # Menus
        self.menuFile = QtWidgets.QMenu("File")
        self.menuMode = QtWidgets.QMenu("Mode")
        self.menuTab = QtWidgets.QMenu("Workstations")  # Default
        self.menuTools = QtWidgets.QMenu("Tools")
        self.menuHelp = QtWidgets.QMenu("Help")

        self.menus = [self.menuFile, self.menuMode, self.menuTab, self.menuTools, self.menuHelp]
        self.update_menu_bar()

    def switch_tab(self, tab_name):
        """Switch to the selected tab and update both left and right panels."""
        # Update Tab Button States
        for tab, button in self.tabButtons.items():
            button.setChecked(tab == tab_name)

        # Update the Right Panel
        if tab_name in self.tabPages:
            self.rightPanel.setCurrentWidget(self.tabPages[tab_name])

        # Update the Left Panel
        if tab_name in self.leftTabPages:
            self.leftPanelContent.setCurrentWidget(self.leftTabPages[tab_name])

        # Update Menu Bar
        self.menuTab.setTitle(tab_name)  # Update the central tab name in the menu bar
        self.update_menu_bar()

    def show_console(self):
        """Show the Console Page without affecting the tabs."""
        self.rightPanel.setCurrentWidget(self.consolePage)

    def switch_page(self, pc_name):
        """Switch to the selected PC Page."""
        if pc_name in self.pcPages:
            self.rightPanel.setCurrentWidget(self.pcPages[pc_name])
            self.update_menu_bar()

    def update_menu_bar(self):
        """Update the menu bar based on the current context."""
        self.menubar.clear()
        for menu in self.menus:
            self.menubar.addMenu(menu)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
