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


class ConnectionHelper(QObject):
    """辅助类：演示连接和断开信号
    
    用于解决 libpython-clj 中 Clojure 函数 disconnect 的问题
    """
    testSignal = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._connected = False
        self._callback = None
        
    def connect_slot(self, callback):
        """连接槽函数"""
        self.testSignal.connect(callback)
        self._connected = True
        self._callback = callback
        
    def disconnect_slot(self):
        """断开槽函数"""
        if self._connected and self._callback:
            self.testSignal.disconnect(self._callback)
            self._connected = False
            self._callback = None
            return True
        return False
        
    def emit_test(self, msg):
        """触发信号"""
        self.testSignal.emit(msg)
        
    def is_connected(self):
        return self._connected
