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
import time

def heavy_computation(value):
    time.sleep(0.2)
    return value * 2

with ThreadPoolExecutor(max_workers=1) as executor:
    future = executor.submit(heavy_computation, 21)
    result = future.result()
    print(f'Result: {result}')
""", globals())

def run_block_3(value):
    import time
    result = value * 2
    time.sleep(0.2)
    return result
