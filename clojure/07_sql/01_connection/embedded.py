def run_block_1():
    exec(r"""
import os
from PySide6.QtSql import QSqlDatabase
db = QSqlDatabase.database()
db.close()
if os.path.exists('demo.db'):
    os.remove('demo.db')
    print('\n测试数据库已删除')
""", globals())
