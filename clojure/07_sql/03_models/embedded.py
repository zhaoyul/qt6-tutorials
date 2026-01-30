def run_block_1():
    exec(r"""
import os
if os.path.exists('models_demo.db'):
    os.remove('models_demo.db')
    print('测试数据库已删除')
""", globals())
