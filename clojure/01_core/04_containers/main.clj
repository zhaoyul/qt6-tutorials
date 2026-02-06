#!/usr/bin/env clojure -M
;; PySide6 容器类示例 (Clojure + libpython-clj)

(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)

;; 导入模块
(require-python '[PySide6.QtCore :as QtCore :bind-ns])

(defn demonstrate-list-operations
  "列表操作"
  []
  (println "\n=== Python 列表操作 ===")

  ;; 使用 Python 列表
  (let [py-list (py/->py-list ["Red" "Green" "Blue"])]
    (println (str "原始列表: " py-list))
    (py/call-attr py-list "append" "Yellow")
    (println (str "添加后: " py-list))
    (println (str "长度: " (py/call-attr py-list "__len__")))
    (println (str "索引1: " (py/call-attr py-list "__getitem__" 1)))))

(defn demonstrate-map-operations
  "字典/映射操作"
  []
  (println "\n=== Python 字典操作 ===")

  ;; 使用 Python 字典
  (let [py-dict (py/->py-dict {"name" "Qt" "version" 6 "language" "Clojure"})]
    (println (str "原始字典: " py-dict))
    (py/call-attr py-dict "__setitem__" "platform" "macOS")
    (println (str "键值 name: " (py/call-attr py-dict "__getitem__" "name")))
    (println (str "所有键: " (py/call-attr py-dict "keys")))
    (println (str "所有值: " (py/call-attr py-dict "values")))))

(defn demonstrate-set-operations
  "集合操作"
  []
  (println "\n=== Python 集合操作 ===")

  ;; 使用 Python 集合
  (let [py-set (py/->python #{1 2 3 4 5})]
    (println (str "原始集合大小: " (py/call-attr py-set "__len__")))
    (py/call-attr py-set "add" 6)
    (py/call-attr py-set "discard" 2)
    (println (str "修改后大小: " (py/call-attr py-set "__len__")))
    (println (str "包含 3: " (py/call-attr py-set "__contains__" 3)))))

(defn demonstrate-tuple-operations
  "元组操作"
  []
  (println "\n=== Python 元组操作 ===")

  ;; 使用 Python 元组
  (let [py-tuple (py/->py-tuple ["Apple" "Banana" "Cherry"])]
    (println (str "元组: " py-tuple))
    (println (str "长度: " (py/call-attr py-tuple "__len__")))
    (println (str "索引0: " (py/call-attr py-tuple "__getitem__" 0)))))

(defn demonstrate-clojure-to-python
  "Clojure 数据转 Python"
  []
  (println "\n=== Clojure 数据转 Python ===")

  ;; 列表
  (let [py-list (py/->python [1 2 3 4 5])]
    (println (str "Clojure 向量 -> Python 列表，长度: " (py/call-attr py-list "__len__"))))

  ;; 映射
  (let [py-dict (py/->python {:a 1 :b 2 :c 3})]
    (println (str "Clojure 映射 -> Python 字典，键: " (py/call-attr py-dict "keys"))))

  ;; 集合
  (let [py-set (py/->python #{"a" "b" "c"})]
    (println (str "Clojure 集合 -> Python 集合，大小: " (py/call-attr py-set "__len__")))))

(defn demonstrate-python-to-clojure
  "Python 数据转 Clojure"
  []
  (println "\n=== Python 数据转 Clojure ===")

  ;; Python 列表转 Clojure
  (let [py-list (py/->py-list [10 20 30])
        clj-vec (vec py-list)]
    (println (str "Python 列表 -> Clojure 向量: " clj-vec)))

  ;; Python 字典转 Clojure
  (let [py-dict (py/->py-dict {"x" 100 "y" 200})
        clj-map (into {} py-dict)]
    (println (str "Python 字典 -> Clojure 映射: " clj-map))))

(defn -main
  [& args]
  (println "=== PySide6 容器类示例 (Clojure) ===")

  (demonstrate-list-operations)
  (demonstrate-map-operations)
  (demonstrate-set-operations)
  (demonstrate-tuple-operations)
  (demonstrate-clojure-to-python)
  (demonstrate-python-to-clojure)

  (println "\n=== 容器操作要点 ===")
  (println "1. py/->py-list: Clojure -> Python 列表")
  (println "2. py/->py-dict: Clojure -> Python 字典")
  (println "3. py/->py-tuple: Clojure -> Python 元组")
  (println "4. py/->python: 自动类型转换")
  (println "5. vec/into: Python -> Clojure 转换")

  (println "\n=== 完成 ==="))

(-main)
