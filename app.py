import sys
from PySide6.QtWidgets import QApplication
from widget import Widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.startedSelecting.connect(lambda rect: print(f"Selected area: {rect}"))
    widget.cancelledSelecting.connect(lambda: print("Selection cancelled"))
    widget.startedSelecting.connect(app.quit)
    widget.cancelledSelecting.connect(app.quit)
    widget.start()
    sys.exit(app.exec())


