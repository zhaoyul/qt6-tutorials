def run_block_1():
    exec(r"""
import sys
from PySide6.QtGui import QGuiApplication
app = QGuiApplication(sys.argv)
""", globals())
