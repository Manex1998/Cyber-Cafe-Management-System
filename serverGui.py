from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(467, 345)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 471, 301))
        self.tabWidget.setObjectName("tabWidget")
        
        # Tab: Workstations
        self.Workstations = QtWidgets.QWidget()
        self.Workstations.setObjectName("Workstations")
        self.scrollArea = QtWidgets.QScrollArea(self.Workstations)
        self.scrollArea.setGeometry(QtCore.QRect(0, 10, 141, 241))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # Layout inside the scroll area
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        # Example dynamic buttons in the scroll area
        for i in range(20):  # Add 20 example buttons
            button = QtWidgets.QToolButton(self.scrollAreaWidgetContents)
            button.setText(f"PC {i + 1}")
            self.scrollLayout.addWidget(button)

        self.tabWidget.addTab(self.Workstations, "Workstations")

        # Other tabs
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "Cards")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "Clients")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "Services")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tabWidget.addTab(self.tab_6, "Session journal")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "Income journal")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 467, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuMode = QtWidgets.QMenu(self.menubar)
        self.menuMode.setObjectName("menuMode")
        self.menuWorkstations = QtWidgets.QMenu(self.menubar)
        self.menuWorkstations.setObjectName("menuWorkstations")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuMode.menuAction())
        self.menubar.addAction(self.menuWorkstations.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect tab changes to update menu
        self.tabWidget.currentChanged.connect(self.update_menu)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuMode.setTitle(_translate("MainWindow", "Mode"))
        self.menuWorkstations.setTitle(_translate("MainWindow", "Workstations"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))

    def update_menu(self, index):
        """Update the menu bar based on the selected tab."""
        self.menubar.clear()  # Clear existing menus
        if index == 0:  # Workstations Tab
            self.menuWorkstations = self.menubar.addMenu("Workstations")
            self.menuWorkstations.addAction("Add PC")
            self.menuWorkstations.addAction("Remove PC")
        elif index == 1:  # Cards Tab
            self.menuCards = self.menubar.addMenu("Cards")
            self.menuCards.addAction("Add Card")
            self.menuCards.addAction("Remove Card")
        else:
            self.menuFile = self.menubar.addMenu("File")
            self.menuHelp = self.menubar.addMenu("Help")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
