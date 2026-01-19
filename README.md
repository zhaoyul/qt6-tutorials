# Qt6 系统学习项目

本项目通过代码示例系统展示 Qt6 的核心功能，帮助全面学习 Qt6 开发。

## 📚 学习路线图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Qt6 学习路线图                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  第一阶段：基础核心                                                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                      │
│  │  01_core    │───▶│  02_gui     │───▶│ 03_widgets  │                      │
│  │  Qt Core    │    │  Qt GUI     │    │ Qt Widgets  │                      │
│  │  核心功能    │    │  图形基础    │    │  桌面组件   │                       │
│  └─────────────┘    └─────────────┘    └─────────────┘                      │
│        │                                     │                              │
│        ▼                                     ▼                              │
│  第二阶段：现代UI                                                             │
│  ┌─────────────┐    ┌─────────────┐                                         │
│  │  04_qml     │───▶│ 05_quick    │                                         │
│  │  Qt QML     │    │ Qt Quick    │                                         │
│  │  声明式语言  │    │  现代UI     │                                          │
│  └─────────────┘    └─────────────┘                                         │
│        │                                                                    │
│        ▼                                                                    │
│  第三阶段：功能扩展                                                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐   │
│  │ 06_network  │    │  07_sql     │    │08_multimedia│    │  09_test    │   │
│  │ Qt Network  │    │  Qt SQL     │    │Qt Multimedia│    │  Qt Test    │   │
│  │   网络通信   │    │  数据库     │    │   多媒体    │    │   测试框架   │   │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘   │
│                                                                             │
│  第四阶段：高级主题                                                            │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                      │
│  │10_concurrent│    │ 11_3d       │    │ 12_project  │                      │
│  │Qt Concurrent│    │  Qt 3D      │    │  综合项目    │                      │
│  │   并发编程   │    │  3D图形     │    │   实战应用   │                      │
│  └─────────────┘    └─────────────┘    └─────────────┘                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 📁 项目结构

```
qt-demos/
├── 01_core/                    # Qt Core 模块
│   ├── 01_meta_object/         # 元对象系统 (MOC)
│   ├── 02_signals_slots/       # 信号与槽机制
│   ├── 03_properties/          # 属性系统
│   ├── 04_containers/          # 容器类
│   ├── 05_io_system/           # I/O 系统
│   ├── 06_event_loop/          # 事件循环
│   ├── 07_threading/           # 多线程
│   └── 08_timer/               # 定时器
│
├── 02_gui/                     # Qt GUI 模块
│   ├── 01_painting/            # 2D绘图系统
│   ├── 02_images/              # 图像处理
│   ├── 03_fonts/               # 字体系统
│   ├── 04_events/              # GUI事件处理
│   └── 05_window/              # 窗口系统
│
├── 03_widgets/                 # Qt Widgets 模块
│   ├── 01_basic_widgets/       # 基础控件
│   ├── 02_layouts/             # 布局管理
│   ├── 03_dialogs/             # 对话框
│   ├── 04_main_window/         # 主窗口
│   ├── 05_item_views/          # 视图组件
│   ├── 06_graphics_view/       # 图形视图框架
│   └── 07_custom_widgets/      # 自定义控件
│
├── 04_qml/                     # Qt QML 模块
│   ├── 01_basics/              # QML基础语法
│   ├── 02_types/               # QML类型系统
│   ├── 03_javascript/          # JavaScript集成
│   └── 04_cpp_integration/     # C++集成
│
├── 05_quick/                   # Qt Quick 模块
│   ├── 01_items/               # Quick基础元素
│   ├── 02_controls/            # Quick Controls
│   ├── 03_animations/          # 动画系统
│   ├── 04_states/              # 状态与转换
│   └── 05_effects/             # 视觉效果
│
├── 06_network/                 # Qt Network 模块
│   ├── 01_tcp/                 # TCP通信
│   ├── 02_udp/                 # UDP通信
│   ├── 03_http/                # HTTP请求
│   └── 04_websocket/           # WebSocket
│
├── 07_sql/                     # Qt SQL 模块
│   ├── 01_connection/          # 数据库连接
│   ├── 02_queries/             # SQL查询
│   └── 03_models/              # SQL模型
│
├── 08_multimedia/              # Qt Multimedia 模块
│   ├── 01_audio/               # 音频播放
│   ├── 02_video/               # 视频播放
│   └── 03_camera/              # 摄像头
│
├── 09_test/                    # Qt Test 模块
│   ├── 01_unit_test/           # 单元测试
│   └── 02_gui_test/            # GUI测试
│
├── 10_concurrent/              # Qt Concurrent 模块
│   ├── 01_run/                 # QtConcurrent::run
│   ├── 02_map_reduce/          # Map-Reduce
│   └── 03_filter/              # Filter操作
│
├── 11_3d/                      # Qt 3D 模块 (可选)
│   └── 01_basics/              # 3D基础
│
└── 12_project/                 # 综合实战项目
    └── todo_app/               # 待办事项应用
```

## 🔑 核心C++类速查

### Qt Core 核心类
| 类名 | 功能 | 示例位置 |
|------|------|----------|
| `QObject` | 所有Qt对象的基类 | 01_core/01_meta_object |
| `QCoreApplication` | 事件循环 | 01_core/06_event_loop |
| `QString` | Unicode字符串 | 01_core/04_containers |
| `QList` / `QVector` | 动态数组 | 01_core/04_containers |
| `QMap` / `QHash` | 关联容器 | 01_core/04_containers |
| `QFile` / `QDir` | 文件操作 | 01_core/05_io_system |
| `QThread` | 线程 | 01_core/07_threading |
| `QTimer` | 定时器 | 01_core/08_timer |
| `QVariant` | 通用值容器 | 01_core/03_properties |

### Qt GUI 核心类
| 类名 | 功能 | 示例位置 |
|------|------|----------|
| `QGuiApplication` | GUI应用程序 | 02_gui/05_window |
| `QPainter` | 2D绘图 | 02_gui/01_painting |
| `QImage` / `QPixmap` | 图像 | 02_gui/02_images |
| `QFont` | 字体 | 02_gui/03_fonts |
| `QWindow` | 窗口 | 02_gui/05_window |
| `QEvent` | 事件基类 | 02_gui/04_events |

### Qt Widgets 核心类
| 类名 | 功能 | 示例位置 |
|------|------|----------|
| `QApplication` | Widgets应用 | 03_widgets/01_basic |
| `QWidget` | 所有控件基类 | 03_widgets/01_basic |
| `QPushButton` | 按钮 | 03_widgets/01_basic |
| `QLabel` | 标签 | 03_widgets/01_basic |
| `QLineEdit` | 单行输入 | 03_widgets/01_basic |
| `QTextEdit` | 多行文本 | 03_widgets/01_basic |
| `QVBoxLayout` | 垂直布局 | 03_widgets/02_layouts |
| `QHBoxLayout` | 水平布局 | 03_widgets/02_layouts |
| `QMainWindow` | 主窗口 | 03_widgets/04_main_window |
| `QDialog` | 对话框 | 03_widgets/03_dialogs |
| `QTableView` | 表格视图 | 03_widgets/05_item_views |
| `QListView` | 列表视图 | 03_widgets/05_item_views |

### Qt Network 核心类
| 类名 | 功能 | 示例位置 |
|------|------|----------|
| `QTcpSocket` | TCP客户端 | 06_network/01_tcp |
| `QTcpServer` | TCP服务器 | 06_network/01_tcp |
| `QUdpSocket` | UDP通信 | 06_network/02_udp |
| `QNetworkAccessManager` | HTTP请求 | 06_network/03_http |

## 🚀 快速开始

### 环境要求
- Qt 6.5+ (推荐 6.6 或更高)
- CMake 3.16+
- C++17 兼容编译器

### 配置并构建（推荐）
```bash
cmake -S . -B build
cmake --build build -j 8
```

### 构建单个示例
```bash
cd 01_core/01_meta_object
mkdir build && cd build
cmake ..
make
./meta_object_demo
```

### 构建所有示例
```bash
mkdir build && cd build
cmake ..
make
```

### 运行示例
构建完成后，可直接运行对应可执行文件（在构建目录的子目录中）：
```bash
./build/01_core/01_meta_object/meta_object_demo
```

也可以单独构建目标：
```bash
cmake --build build --target meta_object_demo
./build/01_core/01_meta_object/meta_object_demo
```

> 如果 CMake 找不到 Qt，请在配置时指定 Qt 安装路径，例如：
> `cmake -S . -B build -DCMAKE_PREFIX_PATH=/path/to/Qt/6.x.x`

### Emacs：快速编译当前示例
仓库内的 `.dir-locals.el` 会在 Emacs 里打开 `main.cpp` 时自动设置 `compile-command`，让你直接 `M-x compile` 就能编译并运行当前示例：
- 仅对 `c++-mode` 且文件名为 `main.cpp` 的缓冲区生效
- 从当前目录的 `CMakeLists.txt` 中解析 `add_executable(...)` 的目标名
- 使用仓库根目录下的 `build/`，生成命令：
  - `cmake --build <root>/build --target <target> -j 8 && <root>/build/<rel>/<target>`

## 📖 学习建议

1. **按顺序学习**：从 01_core 开始，逐步深入
2. **动手实践**：修改示例代码，观察效果变化
3. **阅读文档**：每个示例都有对应的官方文档链接
4. **理解原理**：信号槽机制和元对象系统是核心

## 🔗 官方资源

- [Qt 6 Documentation](https://doc.qt.io/qt-6/)
- [Qt Examples](https://doc.qt.io/qt-6/qtexamplesandtutorials.html)
- [Qt Forum](https://forum.qt.io/)
