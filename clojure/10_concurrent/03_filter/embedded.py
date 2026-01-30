def run_block_1():
    exec(r"""
from PySide6.QtCore import QCoreApplication
import sys
if not QCoreApplication.instance():
    _app = QCoreApplication(sys.argv)
""", globals())

def run_block_2():
    exec(r"""
from concurrent.futures import ThreadPoolExecutor, as_completed

def is_even(value):
    return value % 2 == 0

numbers = list(range(1, 11))

with ThreadPoolExecutor() as executor:
    futures = {executor.submit(is_even, n): n for n in numbers}
    
    even_numbers = []
    for future in as_completed(futures):
        number = futures[future]
        if future.result():
            even_numbers.append(number)
    
    even_numbers.sort()

print(f'Even numbers: {even_numbers}')
""", globals())
