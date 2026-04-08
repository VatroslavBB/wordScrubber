import sys
from PySide6.QtCore import QRect
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication
from widget import Widget

def captureSelectedArea(rect):
    screen = QGuiApplication.screenAt(rect.center())
    if screen is None:
        screen = QGuiApplication.primaryScreen()
    if screen is None:
        print("No screen found for the selected area.")
        return
    
    geometry = screen.geometry()

    x = rect.x() - geometry.x()
    y = rect.y() - geometry.y()
    width = rect.width()
    height = rect.height()

    pic = screen.grabWindow(0, x, y, width, height)
    if pic.isNull():
        print("Failed to capture the selected area.")
        return
    pic.save("screenshot.png")
    print("Selected area captured and saved as screenshot.png")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.startedSelecting.connect(lambda rect: captureSelectedArea(rect))
    widget.cancelledSelecting.connect(lambda: print("Selection cancelled"))
    widget.startedSelecting.connect(app.quit)
    widget.cancelledSelecting.connect(app.quit)
    widget.start()
    sys.exit(app.exec())


