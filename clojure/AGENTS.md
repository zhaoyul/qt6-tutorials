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

## 当前示例覆盖情况（截至 2026-02-06）
说明：以下每个子目录均对应一个可运行的命名空间（位于 `src/qt6_tutorials/...`），并在 `deps.edn` 中提供同名 alias，可直接 `clj -M:<alias>` 运行。

- 01_core: 01_meta_object, 02_signals_slots, 03_properties, 04_containers, 05_io_system, 06_event_loop, 07_threading, 08_timer
- 02_gui: 01_painting, 02_images, 03_fonts, 04_events, 05_window
- 03_widgets: 01_basic_widgets, 02_layouts, 03_dialogs, 04_main_window, 05_item_views, 06_graphics_view, 07_custom_widgets
- 04_qml: 01_basics, 02_types, 03_javascript, 04_cpp_integration
- 05_quick: 01_items, 02_controls, 03_animations, 04_states, 05_effects
- 06_network: 01_tcp, 02_udp, 03_http, 04_websocket
- 07_sql: 01_basics, 01_connection, 02_queries, 03_models
- 08_multimedia: 01_audio, 02_video, 03_camera
- 09_test: 01_unit_test, 02_gui_test
- 10_concurrent: 01_run, 01_basics, 02_map_reduce, 03_filter
- 11_3d: 01_basics
- 12_project: todo_app
