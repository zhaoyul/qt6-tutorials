# 第6章：QML 与 Qt Quick 现代UI

QML（Qt Meta Language）是一种声明式语言，用于设计用户界面。Qt Quick 是建立在 QML 基础上的 UI 框架，提供了丰富的可视化组件和动画系统。本章将详细介绍 QML 的语法和 Qt Quick 的使用。

---

## 6.1 QML 基础语法

### 6.1.1 Hello QML

QML 使用类似 JSON 的语法描述 UI 结构：

```qml
// [QML] Main.qml
import QtQuick
import QtQuick.Window

Window {
    width: 640
    height: 480
    visible: true
    title: "Hello QML"
    
    Text {
        anchors.centerIn: parent
        text: "Hello, QML!"
        font.pixelSize: 24
        color: "#3498db"
    }
}
```

```cpp
// [C++] main.cpp - 加载 QML
#include <QGuiApplication>
#include <QQmlApplicationEngine>

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    
    QQmlApplicationEngine engine;
    engine.load(QUrl(QStringLiteral("qrc:/Main.qml")));
    
    if (engine.rootObjects().isEmpty())
        return -1;
    
    return app.exec();
}
```

```python
# [Python] main.py - 加载 QML
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
import sys

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.load("Main.qml")

if not engine.rootObjects():
    sys.exit(-1)

sys.exit(app.exec())
```

### 6.1.2 基本元素

```qml
// [QML] 基本元素
import QtQuick
import QtQuick.Controls

Rectangle {
    width: 400
    height: 300
    color: "#f0f0f0"
    
    // ID 用于引用
    id: root
    
    // 属性
    property int clickCount: 0
    property string userName: "Guest"
    
    // 信号
    signal userClicked(string name)
    
    // 函数
    function greet() {
        return "Hello, " + userName + "!"
    }
    
    // 子元素
    Text {
        id: titleText
        text: greet()
        font.pixelSize: 24
        anchors.top: parent.top
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 20
    }
    
    Button {
        id: clickButton
        text: "Click me (" + clickCount + ")"
        anchors.centerIn: parent
        
        onClicked: {
            clickCount++
            userClicked(userName)
        }
    }
    
    // 状态
    states: [
        State {
            name: "clicked"
            when: clickCount > 5
            PropertyChanges {
                target: root
                color: "lightblue"
            }
            PropertyChanges {
                target: titleText
                text: "Keep clicking!"
            }
        }
    ]
    
    // 过渡动画
    transitions: [
        Transition {
            from: "*"
            to: "clicked"
            ColorAnimation { duration: 500 }
        }
    ]
}
```

### 6.1.3 锚点布局

```qml
// [QML] 锚点布局
import QtQuick

Rectangle {
    width: 600
    height: 400
    
    // 顶部栏
    Rectangle {
        id: header
        height: 50
        color: "#3498db"
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        
        Text {
            text: "Header"
            color: "white"
            anchors.centerIn: parent
            font.pixelSize: 18
        }
    }
    
    // 左侧边栏
    Rectangle {
        id: sidebar
        width: 150
        color: "#2c3e50"
        anchors.top: header.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
    }
    
    // 主内容区
    Rectangle {
        id: content
        color: "#ecf0f1"
        anchors.top: header.bottom
        anchors.bottom: parent.bottom
        anchors.left: sidebar.right
        anchors.right: parent.right
        anchors.margins: 10
        
        Text {
            text: "Main Content"
            anchors.centerIn: parent
        }
    }
}
```

---

## 6.2 QML 类型系统

### 6.2.1 基本类型

```qml
// [QML] 基本类型
import QtQuick

Item {
    // 数值类型
    property int intValue: 42
    property real realValue: 3.14
    property double doubleValue: 2.718281828
    
    // 字符串
    property string text: "Hello QML"
    property string multiLine: "Line 1\nLine 2\nLine 3"
    
    // 布尔值
    property bool enabled: true
    
    // 列表
    property var numberList: [1, 2, 3, 4, 5]
    property var mixedList: [1, "two", 3.0, true]
    
    // 对象
    property var person: {
        "name": "Alice",
        "age": 30,
        "city": "Beijing"
    }
    
    // 颜色
    property color primaryColor: "#3498db"
    property color secondaryColor: Qt.rgba(0.2, 0.6, 0.4, 1.0)
    property color transparentRed: "#80FF0000"
    
    // 日期时间
    property date currentDate: new Date()
    
    // URL
    property url imageSource: "images/logo.png"
    
    // 枚举值
    property int hAlignment: Qt.AlignHCenter
    
    Component.onCompleted: {
        console.log("int:", intValue)
        console.log("person.name:", person.name)
        console.log("color:", primaryColor)
        
        // 访问列表
        for (var i = 0; i < numberList.length; i++) {
            console.log(numberList[i])
        }
    }
}
```

### 6.2.2 自定义类型

```qml
// [QML] CustomButton.qml
import QtQuick
import QtQuick.Controls

Button {
    id: control
    
    // 自定义属性
    property color primaryColor: "#3498db"
    property color hoverColor: "#2980b9"
    property color pressedColor: "#21618c"
    
    // 样式
    background: Rectangle {
        implicitWidth: 100
        implicitHeight: 40
        color: control.pressed ? pressedColor : 
               (control.hovered ? hoverColor : primaryColor)
        radius: 4
        
        Behavior on color {
            ColorAnimation { duration: 150 }
        }
    }
    
    contentItem: Text {
        text: control.text
        font: control.font
        color: "white"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }
}
```

使用自定义类型：

```qml
// [QML] 使用自定义组件
import QtQuick
import QtQuick.Window

Window {
    width: 400
    height: 300
    visible: true
    
    Column {
        anchors.centerIn: parent
        spacing: 10
        
        CustomButton {
            text: "Primary"
            primaryColor: "#3498db"
        }
        
        CustomButton {
            text: "Success"
            primaryColor: "#27ae60"
            hoverColor: "#229954"
            pressedColor: "#1e8449"
        }
        
        CustomButton {
            text: "Danger"
            primaryColor: "#e74c3c"
            hoverColor: "#c0392b"
            pressedColor: "#922b21"
        }
    }
}
```

---

## 6.3 JavaScript 集成

### 6.3.1 JavaScript 在 QML 中的使用

```qml
// [QML] JavaScript 集成
import QtQuick
import QtQuick.Controls
import "MathUtils.js" as MathUtils

Rectangle {
    width: 600
    height: 400
    
    // JavaScript 函数
    function calculateArea(width, height) {
        return width * height
    }
    
    function factorial(n) {
        if (n <= 1) return 1
        return n * factorial(n - 1)
    }
    
    // 使用外部 JS 文件
    Component.onCompleted: {
        var result = MathUtils.add(10, 20)
        console.log("10 + 20 =", result)
        
        var avg = MathUtils.average([1, 2, 3, 4, 5])
        console.log("Average:", avg)
    }
    
    Column {
        anchors.centerIn: parent
        spacing: 10
        
        Text {
            text: "Area: " + calculateArea(100, 50)
            font.pixelSize: 18
        }
        
        Text {
            text: "5! = " + factorial(5)
            font.pixelSize: 18
        }
        
        Button {
            text: "Calculate"
            onClicked: {
                var numbers = [10, 20, 30, 40, 50]
                var sum = 0
                
                // 数组方法
                numbers.forEach(function(num) {
                    sum += num
                })
                
                // ES6 箭头函数（如果支持）
                var squared = numbers.map(n => n * n)
                
                console.log("Sum:", sum)
                console.log("Squared:", squared)
            }
        }
    }
}
```

```javascript
// [JavaScript] MathUtils.js
function add(a, b) {
    return a + b
}

function subtract(a, b) {
    return a - b
}

function average(numbers) {
    if (numbers.length === 0) return 0
    var sum = 0
    for (var i = 0; i < numbers.length; i++) {
        sum += numbers[i]
    }
    return sum / numbers.length
}

function max(numbers) {
    return Math.max.apply(null, numbers)
}

function min(numbers) {
    return Math.min.apply(null, numbers)
}
```

---

## 6.4 C++/Python 与 QML 集成

### 6.4.1 向 QML 暴露 C++ 对象

```cpp
// [C++] counter.h
#ifndef COUNTER_H
#define COUNTER_H

#include <QObject>
#include <QQmlEngine>

class Counter : public QObject
{
    Q_OBJECT
    QML_ELEMENT  // 使类在 QML 中可用
    Q_PROPERTY(int count READ count WRITE setCount NOTIFY countChanged)
    
public:
    explicit Counter(QObject *parent = nullptr);
    
    int count() const;
    void setCount(int count);
    
    Q_INVOKABLE void increment();  // 可从 QML 调用
    Q_INVOKABLE void decrement();
    Q_INVOKABLE void reset();
    
signals:
    void countChanged(int count);
    
private:
    int m_count;
};

#endif
```

```cpp
// [C++] counter.cpp
#include "counter.h"

Counter::Counter(QObject *parent) 
    : QObject(parent), m_count(0)
{
}

int Counter::count() const
{
    return m_count;
}

void Counter::setCount(int count)
{
    if (m_count != count) {
        m_count = count;
        emit countChanged(m_count);
    }
}

void Counter::increment()
{
    setCount(m_count + 1);
}

void Counter::decrement()
{
    setCount(m_count - 1);
}

void Counter::reset()
{
    setCount(0);
}
```

```cpp
// [C++] main.cpp
#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include "counter.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);
    
    // 注册类型到 QML
    qmlRegisterType<Counter>("CounterModule", 1, 0, "Counter");
    
    QQmlApplicationEngine engine;
    
    // 或者在根上下文中设置实例
    Counter counter;
    engine.rootContext()->setContextProperty("globalCounter", &counter);
    
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
    
    return app.exec();
}
```

```qml
// [QML] 使用 C++ 对象
import QtQuick
import QtQuick.Controls
import CounterModule 1.0

Window {
    width: 400
    height: 300
    visible: true
    title: "C++ Integration"
    
    // 创建 C++ 对象实例
    Counter {
        id: myCounter
        count: 0
    }
    
    Column {
        anchors.centerIn: parent
        spacing: 20
        
        Text {
            text: "Count: " + myCounter.count
            font.pixelSize: 32
        }
        
        Row {
            spacing: 10
            
            Button {
                text: "-"
                onClicked: myCounter.decrement()
            }
            
            Button {
                text: "Reset"
                onClicked: myCounter.reset()
            }
            
            Button {
                text: "+"
                onClicked: myCounter.increment()
            }
        }
    }
}
```

### 6.4.2 Python 与 QML 集成

```python
# [Python] counter.py
from PySide6.QtCore import QObject, Signal, Property, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType
import sys

class Counter(QObject):
    countChanged = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._count = 0
    
    def get_count(self):
        return self._count
    
    def set_count(self, value):
        if self._count != value:
            self._count = value
            self.countChanged.emit(value)
    
    count = Property(int, get_count, set_count, notify=countChanged)
    
    @Slot()
    def increment(self):
        self.set_count(self._count + 1)
    
    @Slot()
    def decrement(self):
        self.set_count(self._count - 1)
    
    @Slot()
    def reset(self):
        self.set_count(0)

# 注册类型
qmlRegisterType(Counter, "CounterModule", 1, 0, "Counter")

app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()

# 设置全局实例
counter = Counter()
engine.rootContext().setContextProperty("globalCounter", counter)

engine.load("main.qml")

sys.exit(app.exec())
```

---

## 6.5 Qt Quick 控件

### 6.5.1 基本控件

```qml
// [QML] Quick 控件
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "Qt Quick Controls"
    
    menuBar: MenuBar {
        Menu {
            title: "File"
            MenuItem { text: "New" }
            MenuItem { text: "Open" }
            MenuSeparator {}
            MenuItem { text: "Exit" }
        }
        Menu {
            title: "Help"
            MenuItem { text: "About" }
        }
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        
        // 标签
        Label {
            text: "User Information"
            font.pixelSize: 20
            font.bold: true
        }
        
        // 文本输入
        TextField {
            id: nameField
            placeholderText: "Enter your name"
            Layout.fillWidth: true
        }
        
        TextArea {
            id: bioField
            placeholderText: "Enter your bio"
            Layout.fillWidth: true
            Layout.preferredHeight: 100
        }
        
        // 组合框
        ComboBox {
            id: countryCombo
            model: ["China", "USA", "UK", "Japan", "Germany"]
            Layout.fillWidth: true
        }
        
        // 滑块
        Slider {
            id: ageSlider
            from: 18
            to: 100
            value: 25
            Layout.fillWidth: true
        }
        
        Label {
            text: "Age: " + Math.round(ageSlider.value)
        }
        
        // 开关
        Switch {
            id: newsletterSwitch
            text: "Subscribe to newsletter"
        }
        
        // 进度条
        ProgressBar {
            value: 0.7
            Layout.fillWidth: true
        }
        
        // 按钮
        RowLayout {
            Button {
                text: "Submit"
                highlighted: true
                onClicked: {
                    console.log("Name:", nameField.text)
                    console.log("Country:", countryCombo.currentText)
                }
            }
            
            Button {
                text: "Cancel"
                onClicked: Qt.quit()
            }
        }
        
        Item { Layout.fillHeight: true }
    }
}
```

### 6.5.2 样式定制

```qml
// [QML] 自定义样式
import QtQuick
import QtQuick.Controls

ApplicationWindow {
    visible: true
    width: 600
    height: 400
    title: "Custom Style"
    
    // 自定义按钮样式
    component CustomButton: Button {
        id: control
        
        contentItem: Text {
            text: control.text
            font: control.font
            opacity: enabled ? 1.0 : 0.3
            color: control.down ? "#2980b9" : "#3498db"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }
        
        background: Rectangle {
            implicitWidth: 100
            implicitHeight: 40
            opacity: enabled ? 1 : 0.3
            border.color: control.down ? "#2980b9" : "#3498db"
            border.width: 1
            radius: 4
            color: control.down ? "#ecf0f1" : "white"
        }
    }
    
    Column {
        anchors.centerIn: parent
        spacing: 10
        
        CustomButton {
            text: "Primary"
        }
        
        CustomButton {
            text: "Secondary"
            enabled: false
        }
    }
}
```

---

## 6.6 动画系统

### 6.6.1 基础动画

```qml
// [QML] 动画
import QtQuick
import QtQuick.Controls

Rectangle {
    width: 600
    height: 400
    color: "#2c3e50"
    
    Rectangle {
        id: animatedRect
        width: 100
        height: 100
        color: "#3498db"
        radius: 10
        x: 50
        y: 150
        
        // 属性动画
        PropertyAnimation on x {
            to: 450
            duration: 2000
            easing.type: Easing.InOutQuad
            loops: Animation.Infinite
            running: true
        }
        
        // 旋转动画
        RotationAnimation on rotation {
            from: 0
            to: 360
            duration: 3000
            loops: Animation.Infinite
            running: true
        }
        
        // 颜色动画
        SequentialAnimation on color {
            loops: Animation.Infinite
            ColorAnimation { to: "#e74c3c"; duration: 1000 }
            ColorAnimation { to: "#f1c40f"; duration: 1000 }
            ColorAnimation { to: "#3498db"; duration: 1000 }
        }
        
        // 缩放动画
        ScaleAnimator on scale {
            from: 1
            to: 1.5
            duration: 1000
            easing.type: Easing.InOutBack
            loops: Animation.Infinite
            running: true
        }
    }
    
    // 使用 Behavior 的动画
    Rectangle {
        id: hoverRect
        width: 80
        height: 80
        color: "#27ae60"
        x: mouseArea.mouseX - width/2
        y: mouseArea.mouseY - height/2
        
        Behavior on x {
            NumberAnimation { duration: 200; easing.type: Easing.OutQuad }
        }
        Behavior on y {
            NumberAnimation { duration: 200; easing.type: Easing.OutQuad }
        }
    }
    
    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
    }
}
```

### 6.6.2 状态与过渡

```qml
// [QML] 状态与过渡
import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    width: 400
    height: 300
    
    // 定义状态
    states: [
        State {
            name: "normal"
            PropertyChanges { target: box; x: 50; color: "#3498db" }
            PropertyChanges { target: label; text: "Normal" }
        },
        State {
            name: "expanded"
            PropertyChanges { target: box; x: 200; color: "#e74c3c"; scale: 1.5 }
            PropertyChanges { target: label; text: "Expanded"; font.pixelSize: 24 }
        }
    ]
    
    // 初始状态
    state: "normal"
    
    // 过渡动画
    transitions: [
        Transition {
            from: "normal"
            to: "expanded"
            SequentialAnimation {
                NumberAnimation { properties: "x"; duration: 500; easing.type: Easing.InOutQuad }
                ColorAnimation { duration: 300 }
                NumberAnimation { properties: "scale"; duration: 300; easing.type: Easing.OutBack }
            }
        },
        Transition {
            from: "expanded"
            to: "normal"
            ParallelAnimation {
                NumberAnimation { properties: "x,scale"; duration: 500; easing.type: Easing.InOutQuad }
                ColorAnimation { duration: 300 }
            }
        }
    ]
    
    Rectangle {
        id: box
        width: 100
        height: 100
        y: 100
        radius: 10
        
        Text {
            id: label
            anchors.centerIn: parent
            color: "white"
            font.pixelSize: 16
        }
        
        MouseArea {
            anchors.fill: parent
            onClicked: {
                root.state = (root.state === "normal") ? "expanded" : "normal"
            }
        }
    }
    
    Button {
        text: "Toggle State"
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 20
        onClicked: root.state = (root.state === "normal") ? "expanded" : "normal"
    }
}
```

---

## 6.7 本章小结

本章介绍了 QML 和 Qt Quick 的核心概念：

| 主题 | 关键内容 | 主要用途 |
|------|----------|----------|
| QML 语法 | 元素、属性、信号 | 声明式 UI |
| 类型系统 | 基本类型、自定义类型 | 数据建模 |
| JavaScript | 内置函数、外部文件 | 业务逻辑 |
| C++/Python 集成 | QML_ELEMENT、qmlRegisterType | 前后端通信 |
| Quick 控件 | Button、TextField、Slider | 现代 UI |
| 动画 | PropertyAnimation、Behavior | 视觉效果 |
| 状态 | states、transitions | 交互设计 |

QML 和 Qt Quick 特别适合需要丰富动画和现代化 UI 的跨平台应用程序开发。
