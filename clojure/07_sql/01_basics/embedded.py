def run_block_1():
    exec(r"""
import sqlite3
import os

# 创建内存数据库或文件数据库
db_path = '/tmp/clojure_test.db'

# 如果存在则删除
if os.path.exists(db_path):
    os.remove(db_path)

# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建表
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        age INTEGER
    )
''')

# 插入数据
users = [
    ('张三', 'zhangsan@example.com', 25),
    ('李四', 'lisi@example.com', 30),
    ('王五', 'wangwu@example.com', 28)
]

cursor.executemany('INSERT INTO users (name, email, age) VALUES (?, ?, ?)', users)
conn.commit()

print(f'插入了 {cursor.rowcount} 条记录')
conn.close()
""", globals())

def run_block_2():
    exec(r"""
import sqlite3

db_path = '/tmp/clojure_test.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 查询所有用户
print('所有用户:')
cursor.execute('SELECT * FROM users')
for row in cursor.fetchall():
    print(f'  ID:{row[0]} 名字:{row[1]} 邮箱:{row[2]} 年龄:{row[3]}')

# 条件查询
print('\n年龄大于25的用户:')
cursor.execute('SELECT * FROM users WHERE age > 25')
for row in cursor.fetchall():
    print(f'  {row[1]} ({row[3]}岁)')

# 聚合查询
print('\n统计:')
cursor.execute('SELECT COUNT(*), AVG(age) FROM users')
count, avg_age = cursor.fetchone()
print(f'  总人数: {count}, 平均年龄: {avg_age:.1f}')

conn.close()
""", globals())

def run_block_3():
    exec(r"""
import sqlite3

db_path = '/tmp/clojure_test.db'
conn = sqlite3.connect(db_path)

try:
    # 开始事务
    conn.execute('BEGIN TRANSACTION')
    
    # 插入数据
    conn.execute('INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
                 ('赵六', 'zhaoliu@example.com', 35))
    conn.execute('INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
                 ('钱七', 'qianqi@example.com', 32))
    
    # 提交事务
    conn.commit()
    print('事务提交成功')
    
except Exception as e:
    # 回滚事务
    conn.rollback()
    print(f'事务回滚: {e}')

conn.close()
""", globals())

def run_block_4():
    exec(r"""
from PySide6.QtSql import QSqlDatabase, QSqlQuery

# 添加数据库
db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('/tmp/clojure_test.db')

if db.open():
    print('Qt SQL 数据库连接成功')
    
    # 执行查询
    query = QSqlQuery()
    if query.exec('SELECT name, age FROM users ORDER BY age'):
        print('用户列表 (按年龄排序):')
        while query.next():
            name = query.value(0)
            age = query.value(1)
            print(f'  {name}: {age}岁')
    else:
        print(f'查询失败: {query.lastError().text()}')
    
    db.close()
else:
    print('数据库连接失败')
""", globals())

def run_block_5():
    exec(r"""
import os
db_path = '/tmp/clojure_test.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print('\n临时数据库已清理')
""", globals())
