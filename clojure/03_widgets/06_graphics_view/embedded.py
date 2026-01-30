def run_block_1():
    exec(r"""
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsScene, QGraphicsView,
    QGraphicsItem, QToolBar
)
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QAction
from PySide6.QtCore import Qt
import sys

class ZoomView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing)

    def wheelEvent(self, event):
        factor = 1.2 if event.angleDelta().y() > 0 else 0.8
        self.scale(factor, factor)

app = QApplication(sys.argv)
win = QMainWindow()
win.setWindowTitle('PySide6 Graphics View Demo')
win.resize(800, 600)

scene = QGraphicsScene(-300, -200, 600, 400, win)
scene.setBackgroundBrush(QBrush(QColor(240, 240, 240)))

rect = scene.addRect(-200, -100, 120, 80, QPen(Qt.blue, 2), QBrush(Qt.cyan))
rect.setFlag(QGraphicsItem.ItemIsMovable)
rect.setFlag(QGraphicsItem.ItemIsSelectable)

ellipse = scene.addEllipse(-40, -120, 100, 80, QPen(Qt.darkGreen, 2), QBrush(Qt.green))
ellipse.setFlag(QGraphicsItem.ItemIsMovable)
ellipse.setFlag(QGraphicsItem.ItemIsSelectable)

line = scene.addLine(120, -120, 220, -40, QPen(Qt.red, 3))
line.setFlag(QGraphicsItem.ItemIsMovable)
line.setFlag(QGraphicsItem.ItemIsSelectable)

text = scene.addText('PySide6 Graphics View', QFont('Arial', 18, QFont.Bold))
text.setPos(-120, 40)
text.setDefaultTextColor(Qt.darkMagenta)
text.setFlag(QGraphicsItem.ItemIsMovable)

view = ZoomView(scene, win)
win.setCentralWidget(view)

toolbar = QToolBar('Zoom', win)
win.addToolBar(toolbar)

zoom_in = QAction('Zoom In', win)
zoom_out = QAction('Zoom Out', win)
reset_zoom = QAction('Reset', win)
zoom_in.triggered.connect(lambda: view.scale(1.2, 1.2))
zoom_out.triggered.connect(lambda: view.scale(0.8, 0.8))
reset_zoom.triggered.connect(view.resetTransform)
toolbar.addAction(zoom_in)
toolbar.addAction(zoom_out)
toolbar.addAction(reset_zoom)

win.show()
app.exec()
""", globals())
