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

        # Split Left and Right Panels (using a QSplitter for proportional resizing)
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.mainLayout.addWidget(self.splitter)

        # Left Panel Layout
        self.leftPanel = QtWidgets.QVBoxLayout()
        self.leftPanelContent = QtWidgets.QStackedWidget()
        self.leftPanel.addWidget(self.leftPanelContent)
        self.leftPanelWidget = QtWidgets.QWidget()
        self.leftPanelWidget.setLayout(self.leftPanel)
        self.splitter.addWidget(self.leftPanelWidget)

        # Right Panel (Dynamic Content)
        self.rightPanel = QtWidgets.QStackedWidget()
        self.splitter.addWidget(self.rightPanel)

        # Set the size ratio of 1:3 for left and right panels
        self.splitter.setSizes([250, 750])  # Left is 250px, Right is 750px (1:3 ratio)

        # Console Button (above the scroll area)
        self.consoleButton = QtWidgets.QPushButton("Console")
        self.consoleButton.setFixedHeight(50)
        self.consoleButton.clicked.connect(self.show_console)

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
            page = self.create_bordered_page(f"{tab} Page")
            self.tabPages[tab] = page
            self.rightPanel.addWidget(page)

        # Add Placeholder Pages for PCs
        self.pcPages = {}
        for i in range(20):
            pcPage = self.create_bordered_page(f"PC {i + 1} Information")
            self.pcPages[f"PC {i + 1}"] = pcPage
            self.rightPanel.addWidget(pcPage)

        # Add Console Page
        self.consolePage = self.create_bordered_page("Console Output Here...", is_text_edit=True)
        self.rightPanel.addWidget(self.consolePage)

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

        # Variables to track last selected PC in Workstations
        self.lastSelectedPC = None
        self.currentTab = None

        # Start with Console Page visible in the Workstations tab
        self.rightPanel.setCurrentWidget(self.consolePage)

    def create_bordered_page(self, content, is_text_edit=False):
        """Helper function to create a bordered page with optional text editing."""
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.Box)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        layout = QtWidgets.QVBoxLayout(frame)

        if is_text_edit:
            widget = QtWidgets.QTextEdit()
            widget.setPlainText(content)
        else:
            widget = QtWidgets.QLabel(content)
            widget.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(widget)
        return frame

    def switch_tab(self, tab_name):
        """Switch to the selected tab and update both left and right panels."""
        # Update Tab Button States
        for tab, button in self.tabButtons.items():
            button.setChecked(tab == tab_name)

        # Handle Right Panel Updates
        if tab_name == "Workstations":
            # Restore the last selected PC or default to console
            if self.lastSelectedPC:
                self.rightPanel.setCurrentWidget(self.pcPages[self.lastSelectedPC])
            else:
                self.rightPanel.setCurrentWidget(self.consolePage)
            # Show the Workstations left panel
            self.leftPanelContent.setCurrentWidget(self.workstationsWidget)
        elif tab_name in self.tabPages:
            self.rightPanel.setCurrentWidget(self.tabPages[tab_name])
            # Set a left panel with a boxed frame for other tabs
            page = self.create_bordered_page(f"{tab_name} Left Content")
            self.leftPanelContent.addWidget(page)
            self.leftPanelContent.setCurrentWidget(page)

        # Update current tab tracker
        self.currentTab = tab_name

        # Update Menu Bar
        self.menuTab.setTitle(tab_name)  # Update the central tab name in the menu bar
        self.update_menu_bar()

    def show_console(self):
        """Show the Console Page without affecting the tabs."""
        self.rightPanel.setCurrentWidget(self.consolePage)
        self.lastSelectedPC = None  # Clear the PC selection when console is active

    def switch_page(self, pc_name):
        """Switch to the selected PC Page."""
        if pc_name in self.pcPages:
            self.rightPanel.setCurrentWidget(self.pcPages[pc_name])
            self.lastSelectedPC = pc_name  # Track the last selected PC
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

