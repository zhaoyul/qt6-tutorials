def run_block_1():
    exec(r"""
from PySide6.QtWidgets import QApplication
import sys
if not QApplication.instance():
    _app = QApplication(sys.argv)
""", globals())
