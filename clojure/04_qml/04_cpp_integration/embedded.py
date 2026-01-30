def run_block_1():
    exec(r"""
from PySide6.QtCore import QObject, Property, Signal, Slot

class Counter(QObject):
    valueChanged = Signal()
    stepChanged = Signal()
    limitReached = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
        self._step = 1
        self._min_value = 0
        self._max_value = 100

    @Property(int, notify=valueChanged)
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if self._value != val:
            self._value = max(self._min_value, min(val, self._max_value))
            self.valueChanged.emit()
            if self._value == self._max_value:
                self.limitReached.emit('已达到最大值!')
            elif self._value == self._min_value:
                self.limitReached.emit('已达到最小值!')

    @Property(int, notify=stepChanged)
    def step(self):
        return self._step

    @step.setter
    def step(self, s):
        if self._step != s:
            self._step = s
            self.stepChanged.emit()

    @Property(str, notify=valueChanged)
    def displayText(self):
        return f'当前值: {self._value}'

    @Slot()
    def increment(self):
        print('[Clojure/Python] increment() 被调用')
        self.value = self._value + self._step

    @Slot()
    def decrement(self):
        print('[Clojure/Python] decrement() 被调用')
        self.value = self._value - self._step

    @Slot()
    def reset(self):
        print('[Clojure/Python] reset() 被调用')
        self.value = 0

    @Slot(str, result=str)
    def formatValue(self, prefix):
        return f'{prefix}: {self._value}'
""", globals())
