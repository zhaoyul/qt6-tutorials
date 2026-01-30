def run_block_1():
    exec(r"""
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlError
import os

# 如果存在则删除旧数据库
if os.path.exists('queries_demo.db'):
    os.remove('queries_demo.db')

# 创建数据库连接
db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('queries_demo.db')

if not db.open():
    print(f'数据库连接失败: {db.lastError().text()}')
    connection_success = False
else:
    connection_success = True
""", globals())

def run_block_2():
    exec(r"""
from PySide6.QtSql import QSqlQuery

query = QSqlQuery()
query.exec('DROP TABLE IF EXISTS employees')
query.exec('''
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT,
        salary REAL,
        hire_date DATE
    )
''')
""", globals())

def run_block_3():
    exec(r"""
from PySide6.QtSql import QSqlQuery

query = QSqlQuery()

# 方式1: 直接执行 SQL 语句
query.exec("INSERT INTO employees (name, department, salary, hire_date) "
           "VALUES ('张三', '技术部', 15000.00, '2023-01-15')")
print(f'直接执行: 插入张三, ID: {query.lastInsertId()}')

# 方式2: 位置参数绑定 (?) - 防止 SQL 注入
query.prepare('INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)')
query.addBindValue('李四')
query.addBindValue('市场部')
query.addBindValue(12000.00)
query.addBindValue('2023-03-20')
query.exec()
print(f'位置参数绑定: 插入李四, ID: {query.lastInsertId()}')

# 方式3: 命名参数绑定 (:name) - 更清晰易读
query.prepare("INSERT INTO employees (name, department, salary, hire_date) "
              "VALUES (:name, :dept, :salary, :hire_date)")
query.bindValue(':name', '王五')
query.bindValue(':dept', '财务部')
query.bindValue(':salary', 13000.00)
query.bindValue(':hire_date', '2023-06-10')
query.exec()
print(f'命名参数绑定: 插入王五, ID: {query.lastInsertId()}')

# 方式4: 批量插入 - 使用 bindValue 设置参数值
query.prepare('INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)')

names = ['赵六', '孙七', '周八']
departments = ['技术部', '人事部', '技术部']
salaries = [18000.00, 9000.00, 16000.00]
hire_dates = ['2023-08-01', '2023-09-15', '2023-11-20']

query.addBindValue(names)
query.addBindValue(departments)
query.addBindValue(salaries)
query.addBindValue(hire_dates)

if query.execBatch():
    print(f'批量插入成功: 插入了 {len(names)} 条记录')
else:
    print(f'批量插入失败: {query.lastError().text()}')
""", globals())

def run_block_4():
    exec(r"""
from PySide6.QtSql import QSqlQuery

query = QSqlQuery()

# 1. 简单查询 - 查询所有员工
print('--- 所有员工 ---')
query.exec('SELECT id, name, department, salary FROM employees')
while query.next():
    id = query.value(0)                        # 通过索引获取
    name = query.value('name')                 # 通过字段名获取
    dept = query.value('department')
    salary = query.value('salary')
    print(f'  ID:{id}, 姓名:{name}, 部门:{dept}, 薪资:{salary:.2f}')

# 2. 条件查询 - 使用参数绑定
print()
print('--- 技术部员工 (参数绑定) ---')
query.prepare('SELECT name, salary FROM employees WHERE department = :dept AND salary > :min_salary')
query.bindValue(':dept', '技术部')
query.bindValue(':min_salary', 15000.00)
query.exec()
while query.next():
    print(f"  {query.value('name')}: ¥{query.value('salary'):.2f}")

# 3. 模糊查询 - LIKE
print()
print("--- 姓名包含 '三' 的员工 ---")
query.prepare("SELECT name, department FROM employees WHERE name LIKE :pattern")
query.bindValue(':pattern', '%三%')
query.exec()
while query.next():
    print(f"  {query.value('name')} - {query.value('department')}")

# 4. 聚合查询
print()
print('--- 部门统计 ---')
query.exec('''SELECT department, COUNT(*) as cnt, AVG(salary) as avg_salary 
              FROM employees GROUP BY department ORDER BY avg_salary DESC''')
while query.next():
    print(f"  {query.value('department')}: {query.value('cnt')}人, 平均薪资 ¥{query.value('avg_salary'):.2f}")

# 5. 排序和分页
print()
print('--- 薪资最高的3名员工 ---')
query.exec('SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3')
rank = 1
while query.next():
    print(f"  第{rank}名: {query.value('name')} - ¥{query.value('salary'):.2f}")
    rank += 1
""", globals())

def run_block_5():
    exec(r"""
from PySide6.QtSql import QSqlQuery

query = QSqlQuery()

# 更新前查询
print('更新前:')
query.exec("SELECT name, salary FROM employees WHERE name = '张三'")
if query.next():
    print(f"  {query.value('name')} 当前薪资: ¥{query.value('salary'):.2f}")

# 方式1: 直接更新
query.exec("UPDATE employees SET salary = salary + 2000 WHERE name = '张三'")
print(f'直接更新: 张三加薪2000, 影响行数: {query.numRowsAffected()}')

# 方式2: 参数绑定更新
query.prepare('UPDATE employees SET salary = :new_salary, department = :new_dept WHERE id = :id')
query.bindValue(':new_salary', 14000.00)
query.bindValue(':new_dept', '研发部')
query.bindValue(':id', 2)
if query.exec():
    print(f'参数绑定更新: 李四信息更新, 影响行数: {query.numRowsAffected()}')

# 批量更新
query.prepare('UPDATE employees SET salary = salary * 1.1 WHERE department = ?')
query.addBindValue('技术部')
query.exec()
print(f'批量更新: 技术部全员涨薪10%, 影响行数: {query.numRowsAffected()}')

# 更新后查询
print()
print('更新后所有员工:')
query.exec('SELECT name, department, salary FROM employees ORDER BY id')
while query.next():
    print(f"  {query.value('name')} ({query.value('department')}): ¥{query.value('salary'):.2f}")
""", globals())

def run_block_6():
    exec(r"""
from PySide6.QtSql import QSqlQuery

query = QSqlQuery()

# 删除前统计
query.exec('SELECT COUNT(*) FROM employees')
if query.next():
    print(f"删除前员工总数: {query.value(0)}")

# 方式1: 直接删除
query.exec("DELETE FROM employees WHERE name = '周八'")
print(f'直接删除: 删除周八, 影响行数: {query.numRowsAffected()}')

# 方式2: 参数绑定删除
query.prepare('DELETE FROM employees WHERE salary < :min_salary')
query.bindValue(':min_salary', 10000.00)
if query.exec():
    print(f'条件删除: 删除薪资低于10000的员工, 影响行数: {query.numRowsAffected()}')

# 删除后统计
query.exec('SELECT COUNT(*) FROM employees')
if query.next():
    print(f"删除后员工总数: {query.value(0)}")
""", globals())

def run_block_7():
    exec(r"""
from PySide6.QtSql import QSqlDatabase, QSqlQuery

db = QSqlDatabase.database()
query = QSqlQuery()

# 事务回滚示例
print('--- 事务回滚示例 ---')
db.transaction()
print('事务开始')

query.exec("INSERT INTO employees (name, department, salary) VALUES ('临时员工1', '测试部', 5000)")
print('插入临时员工1')

query.exec("INSERT INTO employees (name, department, salary) VALUES ('临时员工2', '测试部', 6000)")
print('插入临时员工2')

query.exec("UPDATE employees SET salary = salary + 1000 WHERE department = '测试部'")
print('更新测试部薪资')

db.rollback()
print('事务回滚 - 所有操作撤销')

# 验证回滚
query.exec("SELECT COUNT(*) FROM employees WHERE department = '测试部'")
if query.next():
    print(f"测试部员工数: {query.value(0)} (应为0)")

# 事务提交示例
print()
print('--- 事务提交示例 ---')
db.transaction()
print('事务开始')

query.prepare('INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)')
query.addBindValue('新员工A')
query.addBindValue('产品部')
query.addBindValue(11000.00)
query.addBindValue('2024-01-01')
query.exec()
print('插入新员工A')

query.prepare('INSERT INTO employees (name, department, salary, hire_date) VALUES (?, ?, ?, ?)')
query.addBindValue('新员工B')
query.addBindValue('产品部')
query.addBindValue(12000.00)
query.addBindValue('2024-01-01')
query.exec()
print('插入新员工B')

db.commit()
print('事务提交 - 所有操作生效')

# 验证提交
query.exec("SELECT COUNT(*) FROM employees WHERE department = '产品部'")
if query.next():
    print(f"产品部员工数: {query.value(0)} (应为2)")
""", globals())

def run_block_8():
    exec(r"""
from PySide6.QtSql import QSqlQuery

query = QSqlQuery()

# 尝试执行错误的 SQL
if not query.exec('SELECT * FROM non_existent_table'):
    print('查询失败:')
    print(f'  错误文本: {query.lastError().text()}')
    print(f'  错误类型: {query.lastError().type()}')
    print(f'  数据库错误: {query.lastError().databaseText()}')

# 违反约束错误
query.prepare('INSERT INTO employees (name, department, salary) VALUES (:name, :dept, :salary)')
query.bindValue(':name', None)  # NULL 值
query.bindValue(':dept', '测试部')
query.bindValue(':salary', 10000.00)
if not query.exec():
    print(f"\n插入失败 (name 为 NULL): {query.lastError().text()}")
""", globals())

def run_block_9():
    exec(r"""
from PySide6.QtSql import QSqlDatabase
import os

QSqlDatabase.database().close()
if os.path.exists('queries_demo.db'):
    os.remove('queries_demo.db')
    print('\n测试数据库已删除')
""", globals())
