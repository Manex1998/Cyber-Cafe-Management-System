#include <QApplication>
#include <QMainWindow>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPushButton>
#include <QStackedWidget>
#include <QSplitter>
#include <QScrollArea>
#include <QLabel>
#include <QTextEdit>
#include <QMenuBar>
#include <QMenu>
#include <QFrame>

class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    MainWindow(QWidget* parent = nullptr) : QMainWindow(parent) {
        setWindowTitle("MainWindow");
        resize(1000, 600);

        QWidget* centralWidget = new QWidget(this);
        setCentralWidget(centralWidget);
        QVBoxLayout* mainLayout = new QVBoxLayout(centralWidget);

        // Tab Buttons Layout
        QHBoxLayout* tabButtonLayout = new QHBoxLayout();
        QStringList tabs = {"Workstations", "Cards", "Clients", "Services", "Session Journal", "Income Journal"};

        for (const QString& tab : tabs) {
            QPushButton* button = new QPushButton(tab);
            button->setCheckable(true);
            button->setFlat(true);
            tabButtons[tab] = button;
            connect(button, &QPushButton::clicked, this, [=]() { switchTab(tab); });
            tabButtonLayout->addWidget(button);
        }
        mainLayout->addLayout(tabButtonLayout);

        // Splitter for Left and Right Panels
        QSplitter* splitter = new QSplitter(Qt::Horizontal);
        mainLayout->addWidget(splitter);

        // Left Panel
        QWidget* leftPanelWidget = new QWidget();
        QVBoxLayout* leftPanelLayout = new QVBoxLayout(leftPanelWidget);
        leftPanelContent = new QStackedWidget();
        leftPanelLayout->addWidget(leftPanelContent);
        splitter->addWidget(leftPanelWidget);

        // Right Panel
        rightPanel = new QStackedWidget();
        splitter->addWidget(rightPanel);
        splitter->setSizes({250, 750});

        // Console Button
        QPushButton* consoleButton = new QPushButton("Console");
        consoleButton->setFixedHeight(50);
        connect(consoleButton, &QPushButton::clicked, this, &MainWindow::showConsole);

        // Scroll Area for Workstations Tab
        QScrollArea* scrollArea = new QScrollArea();
        scrollArea->setWidgetResizable(true);
        QWidget* scrollContent = new QWidget();
        QVBoxLayout* scrollLayout = new QVBoxLayout(scrollContent);

        for (int i = 0; i < 20; ++i) {
            QPushButton* pcButton = new QPushButton(QString("PC %1").arg(i + 1));
            pcButton->setFixedHeight(50);
            connect(pcButton, &QPushButton::clicked, this, [=]() { switchPage(QString("PC %1").arg(i + 1)); });
            scrollLayout->addWidget(pcButton);
        }
        scrollArea->setWidget(scrollContent);

        // Workstations Widget
        QWidget* workstationsWidget = new QWidget();
        QVBoxLayout* workstationsLayout = new QVBoxLayout(workstationsWidget);
        workstationsLayout->addWidget(consoleButton);
        workstationsLayout->addWidget(scrollArea);
        leftPanelContent->addWidget(workstationsWidget);

        // Add Pages for Tabs in Right Panel
        for (const QString& tab : tabs) {
            QWidget* page = createBorderedPage(tab + " Page");
            tabPages[tab] = page;
            rightPanel->addWidget(page);
        }

        // Add Placeholder Pages for PCs
        for (int i = 0; i < 20; ++i) {
            QString pcName = QString("PC %1").arg(i + 1);
            QWidget* pcPage = createBorderedPage(pcName + " Information");
            pcPages[pcName] = pcPage;
            rightPanel->addWidget(pcPage);
        }

        // Console Page
        consolePage = createBorderedPage("Console Output Here...", true);
        rightPanel->addWidget(consolePage);

        // Menu Bar
        QMenuBar* menuBar = new QMenuBar(this);
        setMenuBar(menuBar);
        QMenu* menuFile = new QMenu("File");
        QMenu* menuMode = new QMenu("Mode");
        menuTab = new QMenu("Workstations");
        QMenu* menuTools = new QMenu("Tools");
        QMenu* menuHelp = new QMenu("Help");

        menus = {menuFile, menuMode, menuTab, menuTools, menuHelp};
        updateMenuBar();

        // Initialize state
        lastSelectedPC.clear();
        currentTab.clear();
        switchTab("Workstations");
    }

private:
    QStackedWidget* leftPanelContent;
    QStackedWidget* rightPanel;
    QWidget* consolePage;
    QMap<QString, QPushButton*> tabButtons;
    QMap<QString, QWidget*> tabPages;
    QMap<QString, QWidget*> pcPages;
    QString lastSelectedPC;
    QString currentTab;
    QMenu* menuTab;
    QList<QMenu*> menus;

    QWidget* createBorderedPage(const QString& content, bool isTextEdit = false) {
        QFrame* frame = new QFrame();
        frame->setFrameShape(QFrame::Box);
        frame->setFrameShadow(QFrame::Raised);
        QVBoxLayout* layout = new QVBoxLayout(frame);

        if (isTextEdit) {
            QTextEdit* textEdit = new QTextEdit();
            textEdit->setPlainText(content);
            layout->addWidget(textEdit);
        } else {
            QLabel* label = new QLabel(content);
            label->setAlignment(Qt::AlignCenter);
            layout->addWidget(label);
        }
        return frame;
    }

    void switchTab(const QString& tabName) {
        for (auto it = tabButtons.begin(); it != tabButtons.end(); ++it) {
            it.value()->setChecked(it.key() == tabName);
        }

        if (tabName == "Workstations") {
            if (!lastSelectedPC.isEmpty() && pcPages.contains(lastSelectedPC)) {
                rightPanel->setCurrentWidget(pcPages[lastSelectedPC]);
            } else {
                rightPanel->setCurrentWidget(consolePage);
            }
            leftPanelContent->setCurrentIndex(0);
        } else if (tabPages.contains(tabName)) {
            rightPanel->setCurrentWidget(tabPages[tabName]);
            QWidget* page = createBorderedPage(tabName + " Left Content");
            leftPanelContent->addWidget(page);
            leftPanelContent->setCurrentWidget(page);
        }

        currentTab = tabName;
        menuTab->setTitle(tabName);
        updateMenuBar();
    }

    void showConsole() {
        rightPanel->setCurrentWidget(consolePage);
        lastSelectedPC.clear();
    }

    void switchPage(const QString& pcName) {
        if (pcPages.contains(pcName)) {
            rightPanel->setCurrentWidget(pcPages[pcName]);
            lastSelectedPC = pcName;
            updateMenuBar();
        }
    }

    void updateMenuBar() {
        menuBar()->clear();
        for (QMenu* menu : menus) {
            menuBar()->addMenu(menu);
        }
    }
};

int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    MainWindow mainWindow;
    mainWindow.show();
    return app.exec();
}
