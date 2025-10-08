class Styles:
    LIGHT_THEME = """
    QMainWindow, QWidget {
        background-color: #F5F5F7;
    }
    QLabel {
        color: #000000;
        font-family: "SF Pro Display";
        font-size: 14px;
    }
    QPushButton {
        background-color: #007AFF;
        color: white;
        font-family: "SF Pro Text";
        font-size: 14px;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
    }
    QPushButton:hover {
        background-color: #0056CC;
    }
    QPushButton:pressed {
        background-color: #003399;
    }
    QTabWidget::pane {
        border: none;
    }
    QTabBar::tab {
        background: #E5E5EA;
        padding: 10px;
        border-radius: 5px;
        min-width: 120px;
    }
    QTabBar::tab:selected {
        background: #007AFF;
        color: white;
    }
    QFrame#drop_area {
        border: 2px dashed #aaa;
        border-radius: 10px;
        background-color: #f5f5f7;
    }
    """

    DARK_THEME = """
    QMainWindow, QWidget {
        background-color: #1D1D1F;
        color: #FFFFFF;
    }
    QLabel {
        color: #FFFFFF;
        font-family: "SF Pro Display";
        font-size: 14px;
    }
    QPushButton {
        background-color: #007AFF;
        color: white;
        font-family: "SF Pro Text";
        font-size: 14px;
        border: none;
        padding: 12px 24px;
        border-radius: 10px;
    }
    QPushButton:hover {
        background-color: #0056CC;
    }
    QPushButton:pressed {
        background-color: #003399;
    }
    QTabWidget::pane {
        border: none;
    }
    QTabBar::tab {
        background: #3A3A3C;
        color: #FFFFFF;
        padding: 10px;
        border-radius: 5px;
        min-width: 120px;
    }
    QTabBar::tab:selected {
        background: #007AFF;
        color: white;
    }
    QFrame#drop_area {
        border: 2px dashed #545458;
        border-radius: 10px;
        background-color: #3A3A3C;
    }
    """
