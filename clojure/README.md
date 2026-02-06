# PySide6 Clojure Examples (via libpython-clj)

使用 [libpython-clj](https://github.com/clj-python/libpython-clj) 调用 PySide6 的 Clojure 示例。

## 前置要求

1. **Clojure CLI 工具** (https://clojure.org/guides/install_clojure)
2. **Python 3.x + PySide6**: `pip install pyside6`
3. **JDK**: 支持 JDK 17-25（测试通过 JDK 25）

## 最小运行示例

```bash
cd clojure
clojure -M:run 01_core/01_meta_object/main.clj
```

如需直接运行：
```bash
cd clojure
clojure -M 01_core/01_meta_object/main.clj
```

## 项目结构

```
clojure/
├── AGENTS.md             # 经验与注意事项
├── README.md             # 本文件
├── deps.edn              # Clojure 依赖配置
├── python.edn            # Python 环境配置
├── classes/              # 运行/编译产物（可忽略）
├── 01_core/              # 核心功能
│   ├── 01_meta_object/
│   ├── 02_signals_slots/
│   ├── 03_properties/
│   ├── 04_containers/
│   ├── 05_io_system/
│   ├── 06_event_loop/
│   ├── 07_threading/
│   └── 08_timer/
├── 02_gui/               # GUI 与绘图
│   ├── 01_painting/
│   ├── 02_images/
│   ├── 03_fonts/
│   ├── 04_events/
│   └── 05_window/
├── 03_widgets/           # Widgets
│   ├── 01_basic_widgets/
│   ├── 02_layouts/
│   ├── 03_dialogs/
│   ├── 04_main_window/
│   ├── 05_item_views/
│   ├── 06_graphics_view/
│   └── 07_custom_widgets/
├── 04_qml/               # QML
│   ├── 01_basics/
│   ├── 02_types/
│   ├── 03_javascript/
│   └── 04_cpp_integration/
├── 05_quick/             # Qt Quick
│   ├── 01_items/
│   ├── 02_controls/
│   ├── 03_animations/
│   ├── 04_states/
│   └── 05_effects/
├── 06_network/           # 网络
│   ├── 01_tcp/
│   ├── 02_udp/
│   ├── 03_http/
│   └── 04_websocket/
├── 07_sql/               # 数据库
│   ├── 01_basics/
│   ├── 01_connection/
│   ├── 02_queries/
│   └── 03_models/
├── 08_multimedia/        # 多媒体
│   ├── 01_audio/
│   ├── 02_video/
│   └── 03_camera/
├── 09_test/              # 测试
│   ├── 01_unit_test/
│   └── 02_gui_test/
├── 10_concurrent/        # 并发
│   ├── 01_run/
│   ├── 01_basics/
│   ├── 02_map_reduce/
│   └── 03_filter/
├── 11_3d/                # 3D
│   └── 01_basics/
└── 12_project/           # 综合项目
    └── todo_app/
```

## 配置

### Python 环境 (python.edn)

```clojure
{:python-executable "/path/to/python3"
 :python-home "/path/to/python"}
```

示例（conda 环境）：
```clojure
{:python-executable "/Users/a123/miniforge/envs/qt6-py/bin/python3"
 :python-home "/Users/a123/miniforge/envs/qt6-py"}
```

## 运行示例

### 方式1: 使用 :run alias（推荐）

```bash
cd clojure

# 使用统一的 :run alias
clojure -M:run 01_core/01_meta_object/main.clj
clojure -M:run 01_core/02_signals_slots/main.clj
clojure -M:run 01_core/03_properties/main.clj
clojure -M:run 01_core/04_containers/main.clj
clojure -M:run 01_core/05_io_system/main.clj
clojure -M:run 01_core/06_event_loop/main.clj
clojure -M:run 01_core/07_threading/main.clj
clojure -M:run 01_core/08_timer/main.clj
clojure -M:run 02_gui/01_painting/main.clj
clojure -M:run 02_gui/02_images/main.clj
clojure -M:run 02_gui/03_fonts/main.clj
clojure -M:run 02_gui/04_events/main.clj
clojure -M:run 02_gui/05_window/main.clj
clojure -M:run 03_widgets/01_basic_widgets/main.clj
clojure -M:run 03_widgets/02_layouts/main.clj
clojure -M:run 03_widgets/03_dialogs/main.clj
clojure -M:run 03_widgets/04_main_window/main.clj
clojure -M:run 03_widgets/05_item_views/main.clj
clojure -M:run 03_widgets/06_graphics_view/main.clj
clojure -M:run 03_widgets/07_custom_widgets/main.clj
clojure -M:run 04_qml/01_basics/main.clj
clojure -M:run 04_qml/02_types/main.clj
clojure -M:run 04_qml/03_javascript/main.clj
clojure -M:run 04_qml/04_cpp_integration/main.clj
clojure -M:run 05_quick/01_items/main.clj
clojure -M:run 05_quick/02_controls/main.clj
clojure -M:run 05_quick/03_animations/main.clj
clojure -M:run 05_quick/04_states/main.clj
clojure -M:run 05_quick/05_effects/main.clj
clojure -M:run 06_network/01_tcp/main.clj
clojure -M:run 06_network/02_udp/main.clj
clojure -M:run 06_network/03_http/main.clj
clojure -M:run 06_network/04_websocket/main.clj
clojure -M:run 07_sql/01_basics/main.clj
clojure -M:run 07_sql/01_connection/main.clj
clojure -M:run 07_sql/02_queries/main.clj
clojure -M:run 07_sql/03_models/main.clj
clojure -M:run 08_multimedia/01_audio/main.clj
clojure -M:run 08_multimedia/02_video/main.clj
clojure -M:run 08_multimedia/03_camera/main.clj
clojure -M:run 09_test/01_unit_test/main.clj
clojure -M:run 09_test/02_gui_test/main.clj
clojure -M:run 10_concurrent/01_run/main.clj
clojure -M:run 10_concurrent/01_basics/main.clj
clojure -M:run 10_concurrent/02_map_reduce/main.clj
clojure -M:run 10_concurrent/03_filter/main.clj
clojure -M:run 11_3d/01_basics/main.clj
clojure -M:run 12_project/todo_app/main.clj
```

### 方式2: 直接运行

```bash
cd clojure
clojure -M 01_core/01_meta_object/main.clj
```

## 示例说明

### 01_core - 核心功能

| 示例               | 说明                                   |
|--------------------|----------------------------------------|
| `01_meta_object`   | QObject 元对象信息、动态属性、信号连接 |
| `02_signals_slots` | 信号槽连接、自定义信号、多槽连接       |
| `03_properties`    | 动态属性、属性变化通知                 |
| `04_containers`    | QStringList、QSettings、容器操作       |
| `05_io_system`     | QFile、QDir、文件信息、路径操作        |
| `06_event_loop`    | 事件循环、定时器事件、自定义事件       |
| `07_threading`     | QThread、QThreadPool、多线程任务       |
| `08_timer`         | QTimer、单次/重复定时器、精确计时      |

### 03_widgets - 控件

| 示例         | 说明                                               |
|--------------|----------------------------------------------------|
| `02_layouts` | QVBoxLayout、QHBoxLayout、QGridLayout、QFormLayout |
| `03_dialogs` | 消息框、输入框、文件对话框                         |

### 06_network - 网络

| 示例      | 说明                                           |
|-----------|------------------------------------------------|
| `03_http` | QNetworkAccessManager、HTTP GET/POST、异步请求 |

### 07_sql - 数据库

| 示例        | 说明                               |
|-------------|------------------------------------|
| `01_basics` | SQLite、SQL 查询、事务处理、Qt SQL |

### 10_concurrent - 并发

| 示例        | 说明                                               |
|-------------|----------------------------------------------------|
| `01_basics` | QThreadPool、Runnable、ThreadPoolExecutor、asyncio |

## libpython-clj 快速参考

### 初始化
```clojure
(require '[libpython-clj2.python :as py])
(py/initialize!)
```

### 导入模块
```clojure
(require '[libpython-clj2.require :refer [require-python]])
(require-python '[PySide6.QtCore :as QtCore :bind-ns])
```

### 获取类
```clojure
(def QObject (py/get-attr QtCore "QObject"))
```

### 创建对象
```clojure
(def obj (QObject))
```

### 调用方法
```clojure
(py/call-attr obj "setProperty" "key" "value")
```

### 连接信号
```clojure
(py/call-attr (py/get-attr button "clicked") "connect" callback-fn)
```

## 与 Python 版本的对比

| Python | Clojure (libpython-clj) |
|--------|------------------------|
| `from PySide6 import QtCore` | `(require-python '[PySide6.QtCore :as QtCore :bind-ns])` |
| `QObject()` | `(def QObject (py/get-attr QtCore "QObject"))` then `(QObject)` |
| `obj.setProperty(k, v)` | `(py/call-attr obj "setProperty" k v)` |
| `button.clicked.connect(slot)` | `(py/call-attr (py/get-attr button "clicked") "connect" slot)` |

## 注意事项

1. **QCoreApplication 创建**：在 macOS 上，通过 Python 代码创建避免 GUI 初始化问题
2. **信号槽**：始终先获取信号对象 `(py/get-attr obj "signal")` 再调用 `connect`
3. **线程等待**：使用带超时的 `wait`，如 `(py/call-attr thread "wait" 2000)`
4. **嵌入 Python**：优先拆成独立 `.py` 文件，用 `require-python :from ...` 加载
