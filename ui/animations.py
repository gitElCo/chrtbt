from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtWidgets import QWidget

def fade_in(widget: QWidget, duration: int = 500):
    """Плавное появление виджета."""
    widget.setGraphicsEffect(None)
    animation = QPropertyAnimation(widget, b"windowOpacity")
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.InOutCubic)
    animation.start()

def fade_out(widget: QWidget, duration: int = 500):
    """Плавное исчезновение виджета."""
    animation = QPropertyAnimation(widget, b"windowOpacity")
    animation.setStartValue(1)
    animation.setEndValue(0)
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.InOutCubic)
    animation.finished.connect(widget.hide)
    animation.start()

def slide_in(widget: QWidget, direction: str = "left", duration: int = 500):
    """Плавное скольжение виджета."""
    geometry = widget.geometry()
    if direction == "left":
        start_geometry = geometry.translated(-geometry.width(), 0)
    elif direction == "right":
        start_geometry = geometry.translated(geometry.width(), 0)
    elif direction == "top":
        start_geometry = geometry.translated(0, -geometry.height())
    else:  # bottom
        start_geometry = geometry.translated(0, geometry.height())

    widget.setGeometry(start_geometry)
    widget.show()

    animation = QPropertyAnimation(widget, b"geometry")
    animation.setStartValue(start_geometry)
    animation.setEndValue(geometry)
    animation.setDuration(duration)
    animation.setEasingCurve(QEasingCurve.OutCubic)
    animation.start()
