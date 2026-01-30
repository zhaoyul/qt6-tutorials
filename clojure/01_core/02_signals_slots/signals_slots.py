from PySide6.QtCore import QObject, Signal


def ensure_app():
    from PySide6.QtCore import QCoreApplication
    import sys
    if not QCoreApplication.instance():
        QCoreApplication(sys.argv)


class Communicate(QObject):
    speak = Signal(str)
    countChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._count = 0

    def speak_message(self, message):
        self.speak.emit(message)

    def increment(self):
        self._count += 1
        self.countChanged.emit(self._count)


class ValueEmitter(QObject):
    valueChanged = Signal(int, str)

    def emit_value(self, num, text):
        self.valueChanged.emit(num, text)
