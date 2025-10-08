from PySide6.QtCore import QPropertyAnimation, QEasingCurve

def fade_in(widget):
    """Анимация появления виджета."""
    widget.setOpacity(0)
    widget.show()
    animation = QPropertyAnimation(widget, b"opacity")
    animation.setDuration(500)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.start()

def slide_in(widget, direction="left"):
    """Анимация скольжения виджета."""
    widget.setOpacity(0)
    widget.show()
    animation = QPropertyAnimation(widget, b"geometry")
    animation.setDuration(500)
    animation.setEasingCurve(QEasingCurve.OutQuad)

    start_pos = widget.geometry()
    if direction == "left":
        start_pos.moveLeft(-start_pos.width())
    elif direction == "right":
        start_pos.moveLeft(widget.parent().width() if widget.parent() else 0)
    elif direction == "top":
        start_pos.moveTop(-start_pos.height())
    elif direction == "bottom":
        start_pos.moveTop(widget.parent().height() if widget.parent() else 0)

    widget.setGeometry(start_pos)
    animation.setEndValue(widget.geometry())

    # Дополнительная анимация прозрачности
    opacity_animation = QPropertyAnimation(widget, b"opacity")
    opacity_animation.setDuration(500)
    opacity_animation.setStartValue(0)
    opacity_animation.setEndValue(1)

    animation.start()
    opacity_animation.start()

def slide_transition(stacked_widget, index):
    """Анимация перехода между страницами в QStackedWidget."""
    current_widget = stacked_widget.currentWidget()
    next_widget = stacked_widget.widget(index)

    # Анимация выхода текущей страницы
    current_animation = QPropertyAnimation(current_widget, b"geometry")
    current_animation.setDuration(500)
    current_animation.setEasingCurve(QEasingCurve.InQuad)

    # Анимация входа следующей страницы
    next_animation = QPropertyAnimation(next_widget, b"geometry")
    next_animation.setDuration(500)
    next_animation.setEasingCurve(QEasingCurve.OutQuad)

    # Начальные позиции
    screen_width = stacked_widget.width()
    current_geom = current_widget.geometry()
    next_geom = next_widget.geometry()

    # Настраиваем анимацию выхода
    if index > stacked_widget.currentIndex():
        current_animation.setStartValue(current_geom)
        current_animation.setEndValue(current_geom.translated(-screen_width, 0))
    else:
        current_animation.setStartValue(current_geom)
        current_animation.setEndValue(current_geom.translated(screen_width, 0))

    # Настраиваем анимацию входа
    if index > stacked_widget.currentIndex():
        next_widget.setGeometry(next_geom.translated(screen_width, 0))
        next_animation.setStartValue(next_geom.translated(screen_width, 0))
    else:
        next_widget.setGeometry(next_geom.translated(-screen_width, 0))
        next_animation.setStartValue(next_geom.translated(-screen_width, 0))

    next_animation.setEndValue(next_geom)

    # Запускаем анимации параллельно
    current_animation.start()
    next_animation.start()

    # В конце анимации меняем страницу
    current_animation.finished.connect(lambda: stacked_widget.setCurrentIndex(index))
