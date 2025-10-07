class MacOSStyles:
    LIGHT_THEME = """
        QMainWindow {
            background-color: #F5F5F7;
            border: none;
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
        QComboBox {
            border: 1px solid #D1D1D6;
            border-radius: 8px;
            padding: 8px;
            background-color: white;
            font-family: "SF Pro Text";
            font-size: 14px;
        }
        QStatusBar {
            font-family: "SF Pro Text";
            font-size: 12px;
            color: #666666;
        }
        QToolTip {
            font-family: "SF Pro Text";
            font-size: 12px;
            background-color: #333333;
            color: white;
            border-radius: 5px;
            padding: 5px;
        }
    """

    DARK_THEME = """
        QMainWindow {
            background-color: #1D1D1F;
            border: none;
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
        QComboBox {
            border: 1px solid #545458;
            border-radius: 8px;
            padding: 8px;
            background-color: #2C2C2E;
            color: white;
            font-family: "SF Pro Text";
            font-size: 14px;
        }
        QStatusBar {
            font-family: "SF Pro Text";
            font-size: 12px;
            color: #999999;
        }
        QToolTip {
            font-family: "SF Pro Text";
            font-size: 12px;
            background-color: #555555;
            color: white;
            border-radius: 5px;
            padding: 5px;
        }
    """
