# PySide6 Clojure Examples (via libpython-clj)

使用 [libpython-clj](https://github.com/clj-python/libpython-clj) 调用 PySide6 的 Clojure 示例。

## 前置要求

1. **Clojure CLI 工具** (https://clojure.org/guides/install_clojure)
2. **Python 3.x + PySide6**: `pip install pyside6`
3. **JDK**: 支持 JDK 17-25（测试通过 JDK 25）

## 最小运行示例

```bash
cd clojure
clj -M:ch01-core-meta-object
```

## 项目结构

```
clojure/
├── AGENTS.md             # 经验与注意事项
├── README.md             # 本文件
├── deps.edn              # Clojure 依赖配置（每个示例都有对应 alias）
├── python.edn            # Python 环境配置
├── classes/              # 运行/编译产物（可忽略）
├── src/                  # Clojure namespaces (qt6_tutorials.*)
├── 01_core/              # 核心功能（Python embedded 模块）
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

每个示例都有对应 alias，命名规则为 `chXX-<section>-<example>`（如 `01_core/02_signals_slots` → `ch01-core-signals-slots`，命名空间为 `qt6_tutorials.ch01.core.signals_slots`），直接运行即可：

```bash
cd clojure
clj -M:ch01-core-meta-object
clj -M:ch02-gui-painting
clj -M:ch06-network-websocket ws://localhost:8080
clj -M:ch12-project-todo-app
```

完整 alias 列表请查看 `deps.edn` 的 `:aliases`。

macOS 提示：GUI 示例需主线程运行，alias 已包含 `-XstartOnFirstThread`。

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
