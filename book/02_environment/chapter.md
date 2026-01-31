# 第2章：环境搭建

本章将详细介绍四种语言（C++、Python、Clojure、Basilisp）的 Qt6 开发环境搭建方法。

---

## 2.1 C++ 环境搭建

### 2.1.1 安装 Qt6

#### 方法1：使用 Qt 在线安装器（推荐）

1. 下载 Qt 在线安装器：
```bash
# macOS
wget https://d13lb3tujbc8s0.cloudfront.net/onlineinstallers/qt-unified-macOS-x64-4.7.0-online.dmg

# Linux
wget https://d13lb3tujbc8s0.cloudfront.net/onlineinstallers/qt-unified-linux-x64-4.7.0-online.run
chmod +x qt-unified-linux-x64-4.7.0-online.run

# Windows
# 下载 qt-unified-windows-x64-4.7.0-online.exe
```

2. 运行安装器，选择：
   - Qt 6.5+ (或最新 LTS 版本)
   - Qt 5 Compatibility Module（可选）
   - Additional Libraries: Qt Network, Qt SQL, Qt Multimedia 等
   - Qt Creator IDE（推荐）

#### 方法2：使用包管理器

**macOS (Homebrew):**
```bash
brew install qt@6
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install qt6-base-dev qt6-tools-dev qt6-tools-dev-tools \
                 libqt6widgets6 libqt6gui6 libqt6core6 \
                 qt6-multimedia-dev qt6-networkauth-dev
```

**Arch Linux:**
```bash
sudo pacman -S qt6-base qt6-tools qt6-multimedia
```

### 2.1.2 安装 CMake

```bash
# macOS
brew install cmake

# Ubuntu
sudo apt install cmake

# Windows
# 下载安装包或使用 Chocolatey: choco install cmake
```

验证安装：
```bash
cmake --version
# 应显示 3.16+ 版本
```

### 2.1.3 验证 C++ 环境

创建测试项目：

```bash
mkdir -p ~/qt-test && cd ~/qt-test

# 创建 CMakeLists.txt
cat > CMakeLists.txt << 'EOF'
cmake_minimum_required(VERSION 3.16)
project(HelloQt LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets)

add_executable(hello main.cpp)
target_link_libraries(hello Qt6::Core Qt6::Gui Qt6::Widgets)
EOF

# 创建 main.cpp
cat > main.cpp << 'EOF'
#include <QApplication>
#include <QPushButton>
#include <QMessageBox>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    
    QPushButton button("Click Me!");
    QObject::connect(&button, &QPushButton::clicked, [&]() {
        QMessageBox::information(nullptr, "Hello", "Qt6 is working!");
    });
    button.show();
    
    return app.exec();
}
EOF

# 构建并运行
cmake -S . -B build
cmake --build build
./build/hello
```

---

## 2.2 Python 环境搭建

### 2.2.1 安装 Python

确保已安装 Python 3.10+：
```bash
python3 --version
```

### 2.2.2 创建虚拟环境

```bash
# 创建项目目录
mkdir -p ~/qt6-python && cd ~/qt6-python

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### 2.2.3 安装 PySide6

```bash
pip install PySide6
```

可选依赖：
```bash
pip install PySide6-Addons  # 额外组件
pip install shiboken6-generator  # 绑定生成器（高级用户）
```

### 2.2.4 验证 Python 环境

创建测试脚本：

```bash
cat > test_qt.py << 'EOF'
from PySide6.QtWidgets import QApplication, QPushButton, QMessageBox

def on_click():
    QMessageBox.information(None, "Hello", "PySide6 is working!")

app = QApplication([])

button = QPushButton("Click Me!")
button.clicked.connect(on_click)
button.show()

app.exec()
EOF

python test_qt.py
```

---

## 2.3 Clojure 环境搭建

### 2.3.1 安装 Java

Clojure 需要 Java 运行时（JDK 11+）：

```bash
# macOS
brew install openjdk@21

# Ubuntu
sudo apt install openjdk-21-jdk

# 验证
java --version
```

### 2.3.2 安装 Clojure CLI

```bash
# macOS/Linux
curl -L -O https://github.com/clojure/brew-install/releases/latest/download/linux-install.sh
chmod +x linux-install.sh
sudo ./linux-install.sh

# macOS (Homebrew)
brew install clojure/tools/clojure

# 验证
clojure --version
```

### 2.3.3 配置项目依赖

创建项目目录和 `deps.edn`：

```bash
mkdir -p ~/qt6-clojure && cd ~/qt6-clojure

cat > deps.edn << 'EOF'
{:paths ["src"]
 :deps {org.clojure/clojure {:mvn/version "1.11.1"}
        clj-python/libpython-clj {:mvn/version "2.025"}}
 :aliases {:run {:main-opts ["-m" "hello-qt"]}}}
EOF

mkdir -p src
```

### 2.3.4 配置 Python 桥接

Clojure 通过 libpython-clj 调用 PySide6，需要配置 Python 路径：

```clojure
;; src/hello_qt.clj
(ns hello-qt
  (:require [libpython-clj2.python :as py]
            [libpython-clj2.require :refer [require-python]]))

(defn -main []
  ;; 初始化 Python
  (py/initialize!)
  
  ;; 导入 PySide6
  (require-python '[PySide6.QtWidgets :as widgets])
  
  (let [app (widgets/QApplication (py/list []))
        button (widgets/QPushButton "Click Me!")]
    (py/call-attr button "show")
    (py/call-attr app "exec")))
```

### 2.3.5 验证 Clojure 环境

```bash
clojure -M:run
```

---

## 2.4 Basilisp 环境搭建

### 2.4.1 安装 Python 依赖

Basilisp 基于 Python，需要先安装：

```bash
mkdir -p ~/qt6-basilisp && cd ~/qt6-basilisp

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装 Basilisp 和 PySide6
pip install basilisp PySide6
```

### 2.4.2 配置 Lisp 入口点

```bash
mkdir -p src

cat > src/hello_qt.lpy << 'EOF'
(ns hello-qt
  (:import [PySide6.QtWidgets QApplication QPushButton QMessageBox]))

(defn on-click []
  (QMessageBox/information nil "Hello" "Basilisp + Qt6 is working!"))

(defn -main []
  (let [app (QApplication [])
        button (QPushButton "Click Me!")]
    (.connect (.clicked button) on-click)
    (.show button)
    (.exec app)))

(-main)
EOF
```

### 2.4.3 运行 Basilisp 程序

```bash
basilisp run src/hello_qt.lpy
```

---

## 2.5 开发工具推荐

### 2.5.1 IDE 选择

| 语言 | 推荐 IDE | 替代方案 |
|------|----------|----------|
| C++ | Qt Creator | CLion, VS Code |
| Python | PyCharm | VS Code + Python 插件 |
| Clojure | Cursive (IntelliJ) | Emacs + CIDER, VS Code + Calva |
| Basilisp | VS Code + Basilisp 插件 | Emacs |

### 2.5.2 Qt Designer

Qt Designer 是一个可视化 UI 设计工具：

```bash
# 通常随 Qt 安装
designer  # 或 designer-qt6
```

Python 用户可以使用：
```bash
pip install pyside6-tools
pyside6-designer
```

### 2.5.3 调试工具

- **C++**: Qt Creator 内置调试器、GDB、LLDB
- **Python**: PDB、PyCharm 调试器
- **Clojure/Basilisp**: REPL 驱动开发、打印调试

---

## 2.6 本章示例汇总

| 语言 | 示例文件 | 运行命令 |
|------|----------|----------|
| C++ | `main.cpp` | `cmake --build build && ./build/hello` |
| Python | `test_qt.py` | `python test_qt.py` |
| Clojure | `src/hello_qt.clj` | `clojure -M:run` |
| Basilisp | `src/hello_qt.lpy` | `basilisp run src/hello_qt.lpy` |

---

环境搭建完成！现在你可以开始 Qt6 的学习之旅了。在下一章中，我们将深入探索 Qt Core 核心模块。
