def run_block_1():
    exec(r"""
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
""", globals())

def run_block_2():
    exec(r"""
from PySide6.QtCore import QObject, Property, Signal

class Person(QObject):
    nameChanged = Signal(str)
    ageChanged = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._name = ''
        self._age = 0
    
    def get_name(self):
        return self._name
    
    def set_name(self, value):
        if self._name != value:
            self._name = value
            self.nameChanged.emit(value)
    
    def get_age(self):
        return self._age
    
    def set_age(self, value):
        if self._age != value:
            self._age = value
            self.ageChanged.emit(value)
    
    name = Property(str, get_name, set_name, notify=nameChanged)
    age = Property(int, get_age, set_age, notify=ageChanged)
""", globals())
