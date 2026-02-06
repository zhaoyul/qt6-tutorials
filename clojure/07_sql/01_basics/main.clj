#!/usr/bin/env clojure -M
;; PySide6 SQL 数据库示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtSql :as QtSql :bind-ns])
(require-python :from "07_sql/01_basics"
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

(defn demonstrate-sqlite-connection
  "SQLite 连接"
  []
  (println "\n=== SQLite 数据库连接 ===")

  ;; 使用 Python 代码操作数据库
  (py/call-attr py-embedded "run_block_1")

  (println "数据库和表创建完成"))

(defn demonstrate-sql-query
  "SQL 查询"
  []
  (println "\n=== SQL 查询 ===")

  (py/call-attr py-embedded "run_block_2")

  (println "查询完成"))

(defn demonstrate-sql-transaction
  "事务处理"
  []
  (println "\n=== 事务处理 ===")

  (py/call-attr py-embedded "run_block_3")

  (println "事务处理完成"))

(defn demonstrate-model-view
  "模型/视图（Qt SQL）"
  []
  (println "\n=== Qt SQL 模型/视图 ===")

  (if (qtsql-available?)
    (do
      ;; 使用 QtSql
      (py/call-attr py-embedded "run_block_4")
      (println "Qt SQL 模型演示完成"))
    (println "Qt SQL 驱动不可用，跳过 QtSql 演示")))

(defn -main
  [& args]
  (println "=== PySide6 SQL 数据库示例 (Clojure) ===")

  (ensure-core-app)

  (demonstrate-sqlite-connection)
  (demonstrate-sql-query)
  (demonstrate-sql-transaction)
  (demonstrate-model-view)

  (println "\n=== SQL 要点 ===")
  (println "1. SQLite: 轻量级本地数据库")
  (println "2. QSqlDatabase: Qt 数据库连接")
  (println "3. QSqlQuery: SQL 查询执行")
  (println "4. 事务: BEGIN/COMMIT/ROLLBACK")
  (println "5. 模型/视图: 数据与UI分离")

  ;; 清理
  (py/call-attr py-embedded "run_block_5")

  (println "\n=== 完成 ==="))

(-main)
