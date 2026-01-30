def run_block_1():
    exec(r"""
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
""", globals())

def run_block_2():
    exec(r"""
from concurrent.futures import ThreadPoolExecutor

def square(value):
    return value * value

numbers = list(range(1, 11))

with ThreadPoolExecutor() as executor:
    # Map phase
    mapped_results = list(executor.map(square, numbers))
    # Reduce phase
    result = sum(mapped_results)

print(f'Sum of squares: {result}')
""", globals())
