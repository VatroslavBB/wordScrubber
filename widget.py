from PySide6.QtCore import Qt, QRect, QPoint, Signal
from PySide6.QtGui import QGuiApplication, QPainter, QColor, QPen
from PySide6.QtWidgets import QWidget

class Widget(QWidget):
    startedSelecting = Signal(QRect)
    cancelledSelecting = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.selectedArea = QRect()
        self.dragging = False
        self.setGeometry(QGuiApplication.primaryScreen().virtualGeometry())

    def start(self):
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.selectedArea = QRect()
        self.dragging = False
        self.showFullScreen()
        self.raise_()
        self.activateWindow()
        self.setFocus()
        self.grabKeyboard()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        if not self.selectedArea.isNull():
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(self.selectedArea, Qt.transparent)
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            painter.setPen(QPen(Qt.red, 2))
            painter.drawRect(self.selectedArea)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPoint = event.position().toPoint()
            self.endPoint = event.position().toPoint()
            self.selectedArea = QRect(self.startPoint, self.endPoint)
            self.dragging = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.endPoint = event.position().toPoint()
            self.selectedArea = QRect(self.startPoint, self.endPoint).normalized()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.dragging:
            self.dragging = False
            self.endPoint = event.position().toPoint()
            self.selectedArea = QRect(self.startPoint, self.endPoint).normalized()
            self.update()

            if self.selectedArea.width() > 2 and self.selectedArea.height() > 2:
                selected = self.selectedArea
                self.releaseKeyboard()
                self.hide()
                self.startedSelecting.emit(selected)
            else:
                self.releaseKeyboard()
                self.hide()
                self.cancelledSelecting.emit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.dragging = False
            self.selectedArea = QRect()
            self.releaseKeyboard()
            self.hide()
            self.cancelledSelecting.emit()
        else:
            super().keyPressEvent(event)


