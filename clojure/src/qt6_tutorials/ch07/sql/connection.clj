;; PySide6 SQL 数据库连接示例 (Clojure + libpython-clj)

(ns qt6_tutorials.ch07.sql.connection)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtSql :as QtSql :bind-ns])
(require-python :from "07_sql/01_connection"
                '[embedded :as py-embedded :bind-ns :reload])
(require-python '[PySide6.QtCore :as QtCore :bind-ns])

;; 获取类
(def QSqlDatabase (py/get-attr QtSql "QSqlDatabase"))
(def QSqlQuery (py/get-attr QtSql "QSqlQuery"))
(def QSqlError (py/get-attr QtSql "QSqlError"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

(defn- qtsql-available?
  []
  (seq (py/call-attr QSqlDatabase "drivers")))

(defn- ensure-core-app
  []
  (let [existing (py/call-attr QCoreApplication "instance")]
    (or existing (QCoreApplication (py/->py-list [])))))

(defn show-available-drivers
  "显示可用数据库驱动"
  []
  (println "=== 可用数据库驱动 ===\n")
  (println (str "驱动列表: " (py/call-attr QSqlDatabase "drivers"))))

(defn create-connection
  "创建数据库连接"
  []
  (println "\n=== 创建数据库连接 ===\n")

  ;; 使用 SQLite (内置，无需安装)
  (def db (py/call-attr-kw QSqlDatabase "addDatabase" ["QSQLITE"] {}))
  (py/call-attr db "setDatabaseName" "demo.db")

  ;; 内存数据库: (py/call-attr db "setDatabaseName" ":memory:")

  (if (py/call-attr db "open")
    (do
      (println "数据库连接成功")
      (println "数据库文件: demo.db")
      true)
    (do
      (println (str "数据库打开失败: " (py/call-attr (py/call-attr db "lastError") "text")))
      false)))

(defn create-tables
  "创建表"
  []
  (println "\n=== 创建表 ===\n")

  (def query (QSqlQuery))

  ;; 删除旧表
  (py/call-attr query "exec" "DROP TABLE IF EXISTS users")
  (py/call-attr query "exec" "DROP TABLE IF EXISTS orders")

  ;; 创建用户表
  (def success (py/call-attr query "exec" "
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        age INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  "))

  (if success
    (println "users 表创建成功")
    (println (str "创建失败: " (py/call-attr (py/call-attr query "lastError") "text"))))

  ;; 创建订单表
  (def success (py/call-attr query "exec" "
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product TEXT,
        amount REAL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
  "))

  (if success
    (println "orders 表创建成功")))

(defn insert-data
  "插入数据"
  []
  (println "\n=== 插入数据 ===\n")

  (def query (QSqlQuery))

  ;; 方式1: 直接执行
  (py/call-attr query "exec" "INSERT INTO users (name, email, age) VALUES ('张三', 'zhang@example.com', 25)")
  (println (str "插入张三, ID: " (py/call-attr query "lastInsertId")))

  ;; 方式2: 预处理语句 (推荐，防 SQL 注入)
  (py/call-attr query "prepare" "INSERT INTO users (name, email, age) VALUES (?, ?, ?)")
  (py/call-attr query "addBindValue" "李四")
  (py/call-attr query "addBindValue" "li@example.com")
  (py/call-attr query "addBindValue" 30)
  (py/call-attr query "exec")
  (println (str "插入李四, ID: " (py/call-attr query "lastInsertId")))

  ;; 方式3: 命名参数
  (py/call-attr query "prepare" "INSERT INTO users (name, email, age) VALUES (:name, :email, :age)")
  (py/call-attr-kw query "bindValue" [":name" "王五"] {})
  (py/call-attr-kw query "bindValue" [":email" "wang@example.com"] {})
  (py/call-attr-kw query "bindValue" [":age" 28] {})
  (py/call-attr query "exec")
  (println (str "插入王五, ID: " (py/call-attr query "lastInsertId")))

  ;; 批量插入订单
  (py/call-attr query "prepare" "INSERT INTO orders (user_id, product, amount) VALUES (?, ?, ?)")

  (def user-ids [1 1 2 3])
  (def products ["手机" "电脑" "平板" "耳机"])
  (def amounts [5999.0 8999.0 3299.0 299.0])

  (py/call-attr query "addBindValue" user-ids)
  (py/call-attr query "addBindValue" products)
  (py/call-attr query "addBindValue" amounts)

  (if (py/call-attr query "execBatch")
    (println "批量插入订单成功")))

(defn query-data
  "查询数据"
  []
  (println "\n=== 查询数据 ===\n")

  (def query (QSqlQuery))

  ;; 简单查询
  (println "--- 所有用户 ---")
  (py/call-attr query "exec" "SELECT * FROM users")
  (loop []
    (when (py/call-attr query "next")
      (def user-id (py/call-attr query "value" 0))
      (def name (py/call-attr query "value" "name"))
      (def email (py/call-attr query "value" "email"))
      (def age (py/call-attr query "value" "age"))
      (println (str "  ID:" user-id ", 姓名:" name ", 邮箱:" email ", 年龄:" age))
      (recur)))

  ;; 条件查询
  (println "\n--- 年龄大于25的用户 ---")
  (py/call-attr query "prepare" "SELECT name, age FROM users WHERE age > ?")
  (py/call-attr query "addBindValue" 25)
  (py/call-attr query "exec")
  (loop []
    (when (py/call-attr query "next")
      (def name (py/call-attr query "value" "name"))
      (def age (py/call-attr query "value" "age"))
      (println (str "  " name ", " age "岁"))
      (recur)))

  ;; 联表查询
  (println "\n--- 用户订单 (JOIN) ---")
  (py/call-attr query "exec" "
    SELECT users.name, orders.product, orders.amount
    FROM orders
    JOIN users ON orders.user_id = users.id
    ORDER BY users.name
  ")
  (loop []
    (when (py/call-attr query "next")
      (def name (py/call-attr query "value" 0))
      (def product (py/call-attr query "value" 1))
      (def amount (py/call-attr query "value" 2))
      (println (str "  " name " 购买了 " product ", ¥" (format "%.2f" amount)))
      (recur)))

  ;; 聚合查询
  (println "\n--- 统计信息 ---")
  (py/call-attr query "exec" "SELECT COUNT(*), AVG(age) FROM users")
  (when (py/call-attr query "next")
    (println (str "  用户数: " (py/call-attr query "value" 0)))
    (println (str "  平均年龄: " (py/call-attr query "value" 1))))

  (py/call-attr query "exec" "SELECT user_id, SUM(amount) as total FROM orders GROUP BY user_id")
  (println "\n--- 各用户消费总额 ---")
  (loop []
    (when (py/call-attr query "next")
      (def user-id (py/call-attr query "value" 0))
      (def total (py/call-attr query "value" 1))
      (println (str "  用户" user-id ": ¥" (format "%.2f" total)))
      (recur))))

(defn update-and-delete
  "更新和删除"
  []
  (println "\n=== 更新和删除 ===\n")

  (def query (QSqlQuery))

  ;; 更新
  (py/call-attr query "prepare" "UPDATE users SET age = age + 1 WHERE name = ?")
  (py/call-attr query "addBindValue" "张三")
  (when (py/call-attr query "exec")
    (println (str "更新成功, 影响行数: " (py/call-attr query "numRowsAffected"))))

  ;; 验证更新
  (py/call-attr query "exec" "SELECT name, age FROM users WHERE name = '张三'")
  (when (py/call-attr query "next")
    (println (str "张三现在" (py/call-attr query "value" "age") "岁")))

  ;; 删除 (演示，不实际删除)
  (println "\n删除语法: DELETE FROM users WHERE id = ?"))

(defn demonstrate-transactions
  "事务处理"
  []
  (println "\n=== 事务处理 ===\n")

  (def db (py/call-attr QSqlDatabase "database"))
  (def query (QSqlQuery))

  ;; 开始事务
  (py/call-attr db "transaction")
  (println "事务开始")

  (py/call-attr query "exec" "INSERT INTO users (name, email, age) VALUES ('临时用户', 'temp@example.com', 20)")
  (println "插入临时用户")

  ;; 回滚事务
  (py/call-attr db "rollback")
  (println "事务回滚")

  ;; 验证回滚
  (py/call-attr query "exec" "SELECT COUNT(*) FROM users WHERE name = '临时用户'")
  (when (py/call-attr query "next")
    (println (str "临时用户数量: " (py/call-attr query "value" 0) " (应为0)")))

  ;; 提交事务示例
  (println "\n提交事务语法: db.commit()"))

(defn show-record-info
  "显示记录信息"
  []
  (println "\n=== 记录信息 ===\n")

  (def query (QSqlQuery "SELECT * FROM users LIMIT 1"))
  (def record (py/call-attr query "record"))

  (println (str "字段数量: " (py/call-attr record "count")))
  (doseq [i (range (py/call-attr record "count"))]
    (def field (py/call-attr record "field" i))
    (println (str "  字段" i ": " (py/call-attr record "fieldName" i) " (" (py/call-attr field "typeID") ")"))))

(defn -main
  [& args]
  (println "=== PySide6 SQL 数据库连接示例 (Clojure) ===")

  (ensure-core-app)
  (show-available-drivers)

  (if (qtsql-available?)
    (do
      (when-not (create-connection)
        (System/exit 1))

      (create-tables)
      (insert-data)
      (query-data)
      (update-and-delete)
      (demonstrate-transactions)
      (show-record-info)

      ;; 清理
      (py/call-attr py-embedded "run_block_1")

      (println "\n=== 完成 ==="))
    (println "Qt SQL 驱动不可用，跳过演示")))
