def run_block_1():
    exec(r"""from PySide6.QtWidgets import QApplication, QPushButton, QWidget
import unittest

class TestGuiDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
    
    def test_button_text(self):
        button = QPushButton()
        button.setText('Hello')
        self.assertEqual(button.text(), 'Hello')
    
    def test_show_hide_widget(self):
        widget = QWidget()
        widget.show()
        self.assertTrue(widget.isVisible())
        widget.hide()
        self.assertFalse(widget.isVisible())
""", globals())

def run_block_2():
    from PySide6.QtWidgets import QApplication
    global app
    app = QApplication.instance() or QApplication([])
    return app
