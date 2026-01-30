# Clojure + libpython-clj2 (PySide6) 经验

## 导入模块的最佳实践
- 优先使用 `require-python` 导入 Python 模块，并加 `:bind-ns` 绑定模块对象：
  - 示例：`(require-python '[PySide6.QtCore :as QtCore :bind-ns])`
- `:bind-ns` 会在当前命名空间绑定一个 **模块对象 var**（如 `QtCore`），便于 `py/get-attr` 取类/常量。
- `:as` 只创建 **Clojure 命名空间别名**，不是 Python 模块对象。

## PySide6 的特殊点
- PySide6 大量成员是 **动态/惰性导出**，`require-python` 扫描不完整。
- `__dir__` 列出来的名字 **不一定** 会被 `require-python` intern 成 Clojure var。
- 因此不要依赖 `:refer` 或 `QtCore/Foo` 访问类，推荐使用 `py/get-attr`。

## 模块 vs 类对象
- **模块对象**：可以用 `require-python` 导入（如 `PySide6.QtCore`）。
- **类对象**：从模块对象里取（如 `(py/get-attr QtCore "QCoreApplication")`）。

## 推荐写法
```clojure
(require '[libpython-clj2.python :as py]
         '[libpython-clj2.require :refer [require-python]])

(py/initialize!)
(require-python '[PySide6.QtCore :as QtCore :bind-ns])

(def QObject (py/get-attr QtCore "QObject"))
(def QCoreApplication (py/get-attr QtCore "QCoreApplication"))
```

## Q(Core|Gui)Application 入参
- Qt 的 Application 构造函数需要 **Python list**：
  - `(QCoreApplication (py/->py-list []))`
  - 避免直接用 `py/->python` 传空向量。
