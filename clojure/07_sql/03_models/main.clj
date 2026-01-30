#!/usr/bin/env clojure -M
;; Qt6 SQL 模型示例 - QSqlTableModel, QSqlQueryModel
;;
;; 主要类：
;; - QSqlQueryModel: 只读查询模型，用于显示查询结果
;; - QSqlTableModel: 可编辑的表格模型，直接操作数据库表
;; - QSqlRelationalTableModel: 关联表格模型（本示例未演示）
;;
;; 本示例演示：
;; - QSqlQueryModel 的只读查询显示
;; - QSqlTableModel 的基本 CRUD 操作
;; - 排序、过滤、数据修改
;; - 提交和回滚修改
;;
;; 官方文档:
;; - https://doc.qt.io/qt-6/qsqlquerymodel.html
;; - https://doc.qt.io/qt-6/qsqltablemodel.html

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtSql :as QtSql :bind-ns])
(require-python :from "07_sql/03_models"
                '[embedded :as py-embedded :bind-ns :reload])
(require-python '[PySide6.QtCore :as QtCore :bind-ns])

;; 获取类
(def QSqlDatabase (py/get-attr QtSql "QSqlDatabase"))
(def QSqlQuery (py/get-attr QtSql "QSqlQuery"))
(def QSqlQueryModel (py/get-attr QtSql "QSqlQueryModel"))
(def QSqlTableModel (py/get-attr QtSql "QSqlTableModel"))
(def QSqlRecord (py/get-attr QtSql "QSqlRecord"))
(def QSqlError (py/get-attr QtSql "QSqlError"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))

(defn- qtsql-available?
  []
  (seq (py/call-attr QSqlDatabase "drivers")))

(defn- ensure-core-app
  []
  (let [existing (py/call-attr QCoreApplication "instance")]
    (or existing (QCoreApplication (py/->py-list [])))))

;; Qt 常量
(def Qt-Horizontal (py/get-attr (py/get-attr QtCore "Qt") "Horizontal"))
(def Qt-DescendingOrder (py/get-attr (py/get-attr QtCore "Qt") "DescendingOrder"))
(def Qt-AscendingOrder (py/get-attr (py/get-attr QtCore "Qt") "AscendingOrder"))
(def OnManualSubmit (py/get-attr QSqlTableModel "OnManualSubmit"))
(def OnFieldChange (py/get-attr QSqlTableModel "OnFieldChange"))
(def OnRowChange (py/get-attr QSqlTableModel "OnRowChange"))

(defn create-connection
  "创建数据库连接"
  []
  (let [db (py/call-attr QSqlDatabase "addDatabase" "QSQLITE")]
    (py/py. db setDatabaseName "models_demo.db")
    (if (py/py. db open)
      true
      (do (println "数据库连接失败:" (py/py. (py/py. db lastError) text))
          false))))

(defn create-table-and-data
  "创建表和数据"
  []
  (let [query (QSqlQuery)]
    ;; 创建产品表
    (py/py. query exec "DROP TABLE IF EXISTS products")
    (py/py. query exec "CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER DEFAULT 0,
            description TEXT
        )")
    
    ;; 插入测试数据
    (py/py. query exec "INSERT INTO products (name, category, price, stock, description) VALUES 
                   ('iPhone 15', '手机', 5999.00, 100, '苹果最新款手机')")
    (py/py. query exec "INSERT INTO products (name, category, price, stock, description) VALUES 
                   ('MacBook Pro', '电脑', 14999.00, 50, '专业级笔记本电脑')")
    (py/py. query exec "INSERT INTO products (name, category, price, stock, description) VALUES 
                   ('iPad Air', '平板', 4799.00, 80, '轻薄平板电脑')")
    (py/py. query exec "INSERT INTO products (name, category, price, stock, description) VALUES 
                   ('AirPods Pro', '耳机', 1999.00, 200, '降噪耳机')")
    (py/py. query exec "INSERT INTO products (name, category, price, stock, description) VALUES 
                   ('小米14', '手机', 3999.00, 150, '高性价比旗舰机')")
    (py/py. query exec "INSERT INTO products (name, category, price, stock, description) VALUES 
                   ('华为Mate60', '手机', 6999.00, 80, '国产高端手机')")
    
    ;; 创建订单表用于联表查询演示
    (py/py. query exec "DROP TABLE IF EXISTS orders")
    (py/py. query exec "CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            order_date DATE,
            customer_name TEXT
        )")
    
    (py/py. query exec "INSERT INTO orders (product_id, quantity, order_date, customer_name) VALUES 
                   (1, 2, '2024-01-15', '客户A')")
    (py/py. query exec "INSERT INTO orders (product_id, quantity, order_date, customer_name) VALUES 
                   (2, 1, '2024-01-16', '客户B')")
    (py/py. query exec "INSERT INTO orders (product_id, quantity, order_date, customer_name) VALUES 
                   (1, 3, '2024-01-17', '客户C')")
    (py/py. query exec "INSERT INTO orders (product_id, quantity, order_date, customer_name) VALUES 
                   (4, 5, '2024-01-18', '客户D')")))

(defn demonstrate-sql-query-model
  "QSqlQueryModel - 只读查询模型"
  []
  (println "\n=== QSqlQueryModel - 只读查询模型 ===\n")
  
  ;; QSqlQueryModel 用于执行任意 SQL 查询并显示结果
  ;; 它是只读的，不能修改数据
  
  (let [model (QSqlQueryModel)]
    
    ;; 1. 简单查询
    (println "--- 所有产品 (简单查询) ---")
    (py/py. model setQuery "SELECT name, category, price, stock FROM products")
    
    ;; 检查查询是否成功
    (if (py/py. (py/py. model lastError) isValid)
      (println "查询错误:" (py/py. (py/py. model lastError) text))
      (do
        ;; 获取记录数
        (let [row-count (py/py. model rowCount)
              col-count (py/py. model columnCount)]
          (println "记录数:" row-count "列数:" col-count)
          
          ;; 打印表头
          (print "表头: ")
          (doseq [col (range col-count)]
            (print (str (py/py. model headerData col Qt-Horizontal) "\t")))
          (println)
          
          ;; 遍历数据
          (doseq [row (range row-count)]
            (doseq [col (range col-count)]
              (let [index (py/py. model index row col)]
                (print (str (py/py. model data index) "\t"))))
            (println)))))
    
    ;; 2. 复杂查询 - 联表查询
    (println "\n--- 订单详情 (联表查询) ---")
    (py/py. model setQuery "SELECT 
            o.id as 订单ID,
            p.name as 产品名称,
            o.quantity as 数量,
            p.price as 单价,
            (o.quantity * p.price) as 总价,
            o.customer_name as 客户
        FROM orders o
        JOIN products p ON o.product_id = p.id
        ORDER BY o.id")
    
    (let [row-count (py/py. model rowCount)]
      (println "订单记录数:" row-count)
      
      ;; 打印表头
      (doseq [col (range (py/py. model columnCount))]
        (print (str (py/py. model headerData col Qt-Horizontal) "\t")))
      (println)
      
      ;; 遍历数据
      (doseq [row (range row-count)]
        (doseq [col (range (py/py. model columnCount))]
          (print (str (py/py. model data (py/py. model index row col)) "\t")))
        (println)))
    
    ;; 3. 聚合查询
    (println "\n--- 分类统计 (聚合查询) ---")
    (py/py. model setQuery "SELECT 
            category as 分类,
            COUNT(*) as 产品数,
            AVG(price) as 平均价格,
            SUM(stock) as 总库存
        FROM products
        GROUP BY category")
    
    (doseq [row (range (py/py. model rowCount))]
      (let [category (py/py. model data (py/py. model index row 0))
            count (py/py. model data (py/py. model index row 1))
            avg-price (py/py. model data (py/py. model index row 2))
            total-stock (py/py. model data (py/py. model index row 3))]
        (println (format "  %s: %s种产品, 平均价格 ¥%.2f, 总库存 %s"
                        category count avg-price total-stock))))
    
    ;; 4. 刷新数据
    (println "\n--- 刷新数据 ---")
    (py/py. model setQuery (py/py. (py/py. model query) executedQuery))
    (println "数据已刷新，当前记录数:" (py/py. model rowCount))))

(defn demonstrate-sql-table-model
  "QSqlTableModel - 可编辑表格模型"
  []
  (println "\n=== QSqlTableModel - 可编辑表格模型 ===\n")
  
  (let [model (QSqlTableModel)]
    (py/py. model setTable "products")
    
    ;; 设置编辑策略
    ;; OnFieldChange: 字段改变立即提交
    ;; OnRowChange: 行改变时提交 (默认)
    ;; OnManualSubmit: 手动提交
    (py/py. model setEditStrategy OnManualSubmit)
    
    ;; 选择数据
    (py/py. model select)
    
    (println "--- 原始数据 ---")
    (println "记录数:" (py/py. model rowCount))
    
    ;; 打印数据
    (doseq [row (range (py/py. model rowCount))]
      (let [record (py/py. model record row)]
        (println (format "  ID:%s, %s, %s, ¥%.2f, 库存:%s"
                        (py/py. record value "id")
                        (py/py. record value "name")
                        (py/py. record value "category")
                        (py/py. record value "price")
                        (py/py. record value "stock")))))
    
    ;; 1. 修改数据
    (println "\n--- 修改数据 ---")
    (let [index (py/py. model index 0 3)  ; 第一行，price 列
          old-price (py/py. model data index)]
      (println "修改前 iPhone 15 价格:" old-price)
      
      (py/py. model setData index 6299.00)
      (println "修改后 iPhone 15 价格: 6299.00 (未提交到数据库)")
      
      ;; 提交修改
      (if (py/py. model submitAll)
        (println "修改已提交到数据库")
        (println "提交失败:" (py/py. (py/py. model lastError) text))))
    
    ;; 2. 插入新记录
    (println "\n--- 插入新记录 ---")
    (let [new-row (py/py. model rowCount)]
      (py/py. model insertRow new-row)
      
      (py/py. model setData (py/py. model index new-row 1) "iPhone 15 Pro")   ; name
      (py/py. model setData (py/py. model index new-row 2) "手机")             ; category
      (py/py. model setData (py/py. model index new-row 3) 8999.00)           ; price
      (py/py. model setData (py/py. model index new-row 4) 60)                ; stock
      (py/py. model setData (py/py. model index new-row 5) "专业版手机")        ; description
      
      (if (py/py. model submitAll)
        (do (println "新记录已插入")
            (py/py. model select))  ; 刷新以获取新ID
        (println "插入失败:" (py/py. (py/py. model lastError) text))))
    
    ;; 3. 使用记录方式插入
    (println "\n--- 使用 QSqlRecord 插入 ---")
    (let [record (py/py. model record)]
      (py/py. record setValue "name" "Apple Watch")
      (py/py. record setValue "category" "穿戴设备")
      (py/py. record setValue "price" 2999.00)
      (py/py. record setValue "stock" 120)
      (py/py. record setValue "description" "智能手表")
      
      (when (py/py. model insertRecord -1 record)  ; -1 表示插入到最后
        (py/py. model submitAll)
        (println "使用 QSqlRecord 插入成功")))
    
    ;; 4. 删除记录
    (println "\n--- 删除记录 ---")
    (py/py. model removeRow 0)
    (when (py/py. model submitAll)
      (println "第一条记录已删除"))
    
    ;; 刷新并显示最终数据
    (py/py. model select)
    (println (format "\n--- 最终数据 (%s条) ---" (py/py. model rowCount)))
    (doseq [row (range (py/py. model rowCount))]
      (let [r (py/py. model record row)]
        (println (format "  %s (%s): ¥%.2f, 库存:%s"
                        (py/py. r value "name")
                        (py/py. r value "category")
                        (py/py. r value "price")
                        (py/py. r value "stock")))))))

(defn demonstrate-filtering-and-sorting
  "过滤和排序"
  []
  (println "\n=== 过滤和排序 ===\n")
  
  (let [model (QSqlTableModel)]
    (py/py. model setTable "products")
    (py/py. model setEditStrategy OnManualSubmit)
    
    ;; 1. 过滤 - 只显示手机
    (println "--- 过滤: 只显示手机 ---")
    (py/py. model setFilter "category = '手机'")
    (py/py. model select)
    
    (println "手机产品数:" (py/py. model rowCount))
    (doseq [row (range (py/py. model rowCount))]
      (let [record (py/py. model record row)]
        (println (format "  %s: ¥%.2f"
                        (py/py. record value "name")
                        (py/py. record value "price")))))
    
    ;; 2. 复杂过滤
    (println "\n--- 过滤: 价格大于5000且库存大于50 ---")
    (py/py. model setFilter "price > 5000 AND stock > 50")
    (py/py. model select)
    
    (doseq [row (range (py/py. model rowCount))]
      (let [record (py/py. model record row)]
        (println (format "  %s: ¥%.2f, 库存:%s"
                        (py/py. record value "name")
                        (py/py. record value "price")
                        (py/py. record value "stock")))))
    
    ;; 3. 排序
    (println "\n--- 排序: 按价格降序 ---")
    (py/py. model setFilter "")  ; 清除过滤
    (py/py. model setSort 3 Qt-DescendingOrder)  ; 第3列(price)降序
    (py/py. model select)
    
    (doseq [row (range (py/py. model rowCount))]
      (let [record (py/py. model record row)]
        (println (format "  %s: ¥%.2f"
                        (py/py. record value "name")
                        (py/py. record value "price")))))
    
    ;; 4. 多字段排序
    (println "\n--- 排序: 先按分类，再按价格 ---")
    (py/py. model setSort 2 Qt-AscendingOrder)   ; category 升序
    ;; 注意：QSqlTableModel 只支持单字段排序，多字段需要自定义查询
    
    ;; 使用 QSqlQueryModel 实现复杂排序
    (let [query-model (QSqlQueryModel)]
      (py/py. query-model setQuery "SELECT name, category, price, stock 
                               FROM products 
                               ORDER BY category ASC, price DESC")
      
      (doseq [row (range (py/py. query-model rowCount))]
        (println (format "  [%s] %s: ¥%.2f"
                        (py/py. query-model data (py/py. query-model index row 1))
                        (py/py. query-model data (py/py. query-model index row 0))
                        (py/py. query-model data (py/py. query-model index row 2))))))))

(defn demonstrate-batch-operations
  "批量操作和事务"
  []
  (println "\n=== 批量操作和事务 ===\n")
  
  (let [model (QSqlTableModel)]
    (py/py. model setTable "products")
    (py/py. model setEditStrategy OnManualSubmit)  ; 必须设为手动提交
    (py/py. model select)
    
    ;; 批量修改库存
    (println "--- 批量修改库存 ---")
    (doseq [row (range (py/py. model rowCount))]
      (let [record (py/py. model record row)
            current-stock (py/py. record value "stock")
            new-stock (+ current-stock 10)]  ; 所有产品库存 +10
        
        (py/py. model setData (py/py. model index row 4) new-stock)
        (println (format "  %s: 库存 %s -> %s"
                        (py/py. record value "name")
                        current-stock new-stock))))
    
    ;; 一次性提交所有修改
    (if (py/py. model submitAll)
      (println "\n批量修改已提交")
      (println "\n批量修改失败:" (py/py. (py/py. model lastError) text)))
    
    ;; 批量插入
    (println "\n--- 批量插入 ---")
    (let [new-products ["华为平板" "联想笔记本" "索尼耳机"]
          categories ["平板" "电脑" "耳机"]
          prices [3299.00 6999.00 2499.00]]
      
      (doseq [i (range (count new-products))]
        (let [row (py/py. model rowCount)]
          (py/py. model insertRow row)
          (py/py. model setData (py/py. model index row 1) (nth new-products i))
          (py/py. model setData (py/py. model index row 2) (nth categories i))
          (py/py. model setData (py/py. model index row 3) (nth prices i))
          (py/py. model setData (py/py. model index row 4) 50)))
      
      (if (py/py. model submitAll)
        (do (println (format "批量插入成功: %s条记录" (count new-products)))
            (py/py. model select)
            (println "当前总记录数:" (py/py. model rowCount))))
      
      ;; 回滚示例
      (println "\n--- 批量回滚示例 ---")
      (let [original-count (py/py. model rowCount)]
        (println "当前记录数:" original-count)
        
        ;; 插入一些临时数据
        (py/py. model insertRow (py/py. model rowCount))
        (py/py. model setData (py/py. model index (- (py/py. model rowCount) 1) 1) "临时产品1")
        (py/py. model insertRow (py/py. model rowCount))
        (py/py. model setData (py/py. model index (- (py/py. model rowCount) 1) 1) "临时产品2")
        
        (println "插入2条临时数据后，行数:" (py/py. model rowCount))
        
        ;; 回滚 - 使用 revertAll()
        (py/py. model revertAll)
        (println "回滚后，行数:" (py/py. model rowCount) "(应恢复为" original-count ")")))))

(defn demonstrate-header-customization
  "表头自定义"
  []
  (println "\n=== 表头自定义 ===\n")
  
  (let [model (QSqlTableModel)]
    (py/py. model setTable "products")
    
    ;; 自定义表头显示
    (py/py. model setHeaderData 0 Qt-Horizontal "编号")
    (py/py. model setHeaderData 1 Qt-Horizontal "产品名称")
    (py/py. model setHeaderData 2 Qt-Horizontal "分类")
    (py/py. model setHeaderData 3 Qt-Horizontal "价格(元)")
    (py/py. model setHeaderData 4 Qt-Horizontal "库存数量")
    (py/py. model setHeaderData 5 Qt-Horizontal "产品描述")
    
    (py/py. model select)
    
    ;; 打印自定义表头
    (println "自定义表头:")
    (doseq [col (range (py/py. model columnCount))]
      (let [header (py/py. model headerData col Qt-Horizontal)
            original (py/py. (py/py. model record) fieldName col)]
        (println (format "  列%s: '%s' (原字段: %s)"
                        col header original))))))

(defn cleanup
  "清理数据库文件"
  []
  (let [db (py/call-attr QSqlDatabase "database")]
    (py/call-attr db "close"))
  (py/call-attr py-embedded "run_block_1"))

(defn -main
  "主函数"
  [& args]
  (println "=== Qt6 SQL 模型示例 (QSqlQueryModel & QSqlTableModel) ===")

  (ensure-core-app)
  (if (qtsql-available?)
    (do
      (when-not (create-connection)
        (System/exit 1))
      
      (create-table-and-data)
      
      (demonstrate-sql-query-model)
      (demonstrate-sql-table-model)
      (demonstrate-filtering-and-sorting)
      (demonstrate-batch-operations)
      (demonstrate-header-customization)
      
      ;; 清理
      (cleanup)
      
      (println "\n=== 完成 ==="))
    (println "Qt SQL 驱动不可用，跳过演示")))

(-main)
