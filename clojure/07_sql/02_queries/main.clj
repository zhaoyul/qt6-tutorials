#!/usr/bin/env clojure -M
;; Qt6 SQL 查询示例 - QSqlQuery (Clojure + libpython-clj)
;;
;; 主要类：
;; - QSqlQuery: SQL 查询执行
;; - QSqlError: 错误处理
;;
;; 本示例演示：
;; - INSERT 插入数据（多种参数绑定方式）
;; - UPDATE 更新数据
;; - DELETE 删除数据
;; - SELECT 查询数据
;; - 批量操作
;; - 事务处理
;;
;; 官方文档: https://doc.qt.io/qtforpython/PySide6/QtSql/index.html

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

(require-python :from "07_sql/02_queries"
                '[embedded :as py-embedded :bind-ns :reload])
(require-python '[PySide6.QtCore :as QtCore :bind-ns])

(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

(defn- ensure-core-app
  []
  (let [existing (py/call-attr QCoreApplication "instance")]
    (or existing (QCoreApplication (py/->py-list [])))))

(defn create-connection
  "创建数据库连接"
  []
  (try
    (ensure-core-app)
    (py/call-attr py-embedded "run_block_1")
    (boolean (py/get-attr py-embedded "connection_success"))
    (catch Exception e
      (println (str "数据库连接失败: " e))
      false)))

(defn create-table
  "创建员工表"
  []
  (py/call-attr py-embedded "run_block_2"))

(defn demonstrate-insert
  "演示 INSERT 插入数据"
  []
  (println "\n=== INSERT 插入数据 ===\n")
  
  (py/call-attr py-embedded "run_block_3"))

(defn demonstrate-select
  "演示 SELECT 查询数据"
  []
  (println "\n=== SELECT 查询数据 ===\n")
  
  (py/call-attr py-embedded "run_block_4"))

(defn demonstrate-update
  "演示 UPDATE 更新数据"
  []
  (println "\n=== UPDATE 更新数据 ===\n")
  
  (py/call-attr py-embedded "run_block_5"))

(defn demonstrate-delete
  "演示 DELETE 删除数据"
  []
  (println "\n=== DELETE 删除数据 ===\n")
  
  (py/call-attr py-embedded "run_block_6"))

(defn demonstrate-transaction
  "演示事务处理"
  []
  (println "\n=== 事务中的增删改查 ===\n")
  
  (py/call-attr py-embedded "run_block_7"))

(defn demonstrate-error-handling
  "演示错误处理"
  []
  (println "\n=== 错误处理 ===\n")
  
  (py/call-attr py-embedded "run_block_8"))

(defn -main
  "主函数"
  [& args]
  (println "=== Qt6 SQL 查询示例 (QSqlQuery) ===")

  (ensure-core-app)
  (if (create-connection)
    (do
      (create-table)
      (demonstrate-insert)
      (demonstrate-select)
      (demonstrate-update)
      (demonstrate-delete)
      (demonstrate-transaction)
      (demonstrate-error-handling)
      
      ;; 清理
      (py/call-attr py-embedded "run_block_9")
      
      (println "\n=== 完成 ==="))
    (println "Qt SQL 驱动不可用或连接失败，跳过演示")))

(-main)
