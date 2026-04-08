import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication
from widget import Widget
from PySide6.QtCore import QObject, Signal

from textRemoval import scrubImage, cv2
import os

from pathlib import Path

from pynput import keyboard

class Bridge(QObject):
    triggerScrub = Signal()

def handleScrubbing(pic):
    outputDir = Path.home() / "Desktop" / "WordScrubberImg"
    outputDir.mkdir(parents=True, exist_ok=True)
    pic.save(str(outputDir / "screenshotQ121.png"))
    image = cv2.imread(str(outputDir / "screenshotQ121.png"))
    scrubImage(image)
    os.remove(str(outputDir / "screenshotQ121.png"))
    return None
    
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
    handleScrubbing(pic)
    print("Selected area captured and saved as screenshot.png")

def globalShortcut(bridge):

    def onActivate():
        bridge.triggerScrub.emit()

    hotkey = keyboard.HotKey(keyboard.HotKey.parse("<ctrl>+<shift>+j"), onActivate)

    def forCanonical(f):
        return lambda k: f(listener.canonical(k))
    
    listener = keyboard.Listener(on_press=forCanonical(hotkey.press), on_release=forCanonical(hotkey.release))
    listener.start()
    return listener


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    bridge = Bridge()
    widget.startedSelecting.connect(lambda rect: captureSelectedArea(rect))
    widget.cancelledSelecting
    bridge.triggerScrub.connect(widget.start)
    listener = globalShortcut(bridge)
    sys.exit(app.exec())


