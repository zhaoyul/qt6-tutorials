# 第3章：Qt Core 核心模块

Qt Core 是所有 Qt 模块的基础，提供了非 GUI 功能的核心类。本章将详细介绍 Qt Core 的主要功能，并在四种语言中展示其实现方式。

---

## 3.1 元对象系统（Meta-Object System）

Qt 的元对象系统是 Qt 的核心特性之一，提供了：
- 信号与槽机制
- 运行时类型信息
- 动态属性系统

### 3.1.1 核心概念

**QObject** 是所有 Qt 对象的基类：

```cpp
// [C++] QObject 基础
#include <QObject>
#include <QDebug>

class MyObject : public QObject
{
    Q_OBJECT  // 必须添加此宏
    
public:
    MyObject(QObject *parent = nullptr) : QObject(parent) {}
    
    void doSomething() {
        qDebug() << "Object name:" << objectName();
        qDebug() << "Class name:" << metaObject()->className();
    }
};
```

```python
# [Python] QObject 基础
from PySide6.QtCore import QObject

class MyObject(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def do_something(self):
        print(f"Object name: {self.objectName()}")
        print(f"Class name: {self.metaObject().className()}")
```

```clojure
;; [Clojure] QObject 基础
(ns meta-object
  (:require [libpython-clj2.python :as py]
            [libpython-clj2.require :refer [require-python]]))

(py/initialize!)
(require-python '[PySide6.QtCore :as QtCore])

(def MyObject
  (py/create-class
    "MyObject"
    [QtCore/QObject]
    {"__init__" (fn [self parent]
                  (py/call-attr-super self "__init__" parent))}))

(let [obj (MyObject nil)]
  (py/call-attr obj "setObjectName" "MyObjectInstance")
  (println "Object name:" (py/call-attr obj "objectName"))
  (println "Class name:" (py/call-attr (py/call-attr obj "metaObject") "className")))
```

```clojure
;; [Basilisp] QObject 基础
(ns meta-object
  (:import [PySide6.QtCore QObject]))

(defclass MyObject [QObject]
  "自定义 QObject 类")

(let [obj (MyObject)]
  (.setObjectName obj "MyObjectInstance")
  (println "Object name:" (.objectName obj))
  (println "Class name:" (.. obj metaObject className)))
```

### 3.1.2 对象树与内存管理

Qt 使用父子对象关系自动管理内存：

```cpp
// [C++] 对象树自动内存管理
QObject *parent = new QObject();
QObject *child1 = new QObject(parent);  // child1 的父对象是 parent
QObject *child2 = new QObject(parent);

// 当 parent 被删除时，child1 和 child2 会自动删除
delete parent;  // 同时删除 child1 和 child2
```

```python
# [Python] 对象树
from PySide6.QtCore import QObject

parent = QObject()
child1 = QObject(parent)  # 设置 parent 为父对象
child2 = QObject(parent)

# Python 有 GC，但 Qt 的父子关系仍然有效
# 当 parent 被删除，child1 和 child2 也会被删除
```

---

## 3.2 信号与槽（Signals & Slots）

信号与槽是 Qt 的核心通信机制，用于对象间的松耦合通信。

### 3.2.1 基础用法

```cpp
// [C++] 定义信号与槽
#include <QObject>

class Counter : public QObject
{
    Q_OBJECT
    
public:
    Counter(QObject *parent = nullptr) : QObject(parent), m_value(0) {}
    
    int value() const { return m_value; }
    
public slots:
    void setValue(int value) {
        if (m_value != value) {
            m_value = value;
            emit valueChanged(value);  // 发射信号
        }
    }
    
signals:
    void valueChanged(int newValue);  // 定义信号
    
private:
    int m_value;
};

// 使用
Counter a, b;
QObject::connect(&a, &Counter::valueChanged,
                 &b, &Counter::setValue);
a.setValue(12);  // a.value == 12, b.value == 12
```

```python
# [Python] 信号与槽
from PySide6.QtCore import QObject, Signal, Slot

class Counter(QObject):
    valueChanged = Signal(int)  # 定义信号
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0
    
    def value(self):
        return self._value
    
    @Slot(int)  # 标记为槽
    def setValue(self, value):
        if self._value != value:
            self._value = value
            self.valueChanged.emit(value)  # 发射信号

# 使用
a = Counter()
b = Counter()

a.valueChanged.connect(b.setValue)  # 连接信号到槽
a.setValue(12)  # a.value() == 12, b.value() == 12
```

```clojure
;; [Clojure] 信号与槽
(ns signals-slots
  (:require [libpython-clj2.python :as py]
            [libpython-clj2.require :refer [require-python]]))

(py/initialize!)
(require-python '[PySide6.QtCore :as QtCore])

;; 创建带信号和槽的类
(def Counter
  (py/create-class
    "Counter"
    [QtCore/QObject]
    {"valueChanged" (QtCore/Signal int)
     "__init__" (fn [self parent]
                  (py/call-attr-super self "__init__" parent)
                  (py/set-attr! self "_value" 0))
     "value" (fn [self] (py/get-attr self "_value"))
     "setValue" (py/with-attr-decorator
                  (QtCore/Slot int)
                  (fn [self value]
                    (when (not= (py/get-attr self "_value") value)
                      (py/set-attr! self "_value" value)
                      (py/call-attr self "valueChanged.emit" value))))}))

(let [a (Counter nil)
      b (Counter nil)]
  ;; 连接信号到槽
  (py/call-attr (py/call-attr a "valueChanged") "connect" 
                (py/get-attr b "setValue"))
  ;; 触发信号
  (py/call-attr a "setValue" 12))
```

```clojure
;; [Basilisp] 信号与槽
(ns signals-slots
  (:import [PySide6.QtCore QObject Signal Slot]))

(defclass Counter [QObject]
  "带信号和槽的计数器"
  (valueChanged (Signal int))
  
  (defn __init__ [self & [parent]]
    (.__init__ (super Counter self) parent)
    (set! (.-_value self) 0))
  
  (defn value [self]
    (.-_value self))
  
  (Slot int)
  (defn setValue [self value]
    (when (not= (.-_value self) value)
      (set! (.-_value self) value)
      (.emit (.valueChanged self) value))))

(let [a (Counter)
      b (Counter)]
  (.connect (.valueChanged a) #(.setValue b %))
  (.setValue a 12))
```

### 3.2.2 连接类型

```cpp
// [C++] 连接类型
// 1. 直接连接（默认）- 同步执行
connect(sender, &Sender::signal, receiver, &Receiver::slot, Qt::DirectConnection);

// 2. 队列连接 - 异步执行
connect(sender, &Sender::signal, receiver, &Receiver::slot, Qt::QueuedConnection);

// 3. 自动连接 - 根据线程自动选择
connect(sender, &Sender::signal, receiver, &Receiver::slot, Qt::AutoConnection);
```

```python
# [Python] 连接类型
from PySide6.QtCore import Qt

# 直接连接
sender.signal.connect(receiver.slot, type=Qt.DirectConnection)

# 队列连接
sender.signal.connect(receiver.slot, type=Qt.QueuedConnection)

# 自动连接（默认）
sender.signal.connect(receiver.slot)  # type=Qt.AutoConnection
```

---

## 3.3 属性系统（Property System）

Qt 的属性系统提供了对对象属性的动态访问。

### 3.3.1 定义属性

```cpp
// [C++] Q_PROPERTY
class Person : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString name READ name WRITE setName NOTIFY nameChanged)
    Q_PROPERTY(int age READ age WRITE setAge NOTIFY ageChanged)
    
public:
    explicit Person(QObject *parent = nullptr) 
        : QObject(parent), m_age(0) {}
    
    QString name() const { return m_name; }
    void setName(const QString &name) {
        if (m_name != name) {
            m_name = name;
            emit nameChanged(name);
        }
    }
    
    int age() const { return m_age; }
    void setAge(int age) {
        if (m_age != age) {
            m_age = age;
            emit ageChanged(age);
        }
    }
    
signals:
    void nameChanged(const QString &name);
    void ageChanged(int age);
    
private:
    QString m_name;
    int m_age;
};

// 使用动态属性
Person person;
person.setProperty("name", "Alice");
QString name = person.property("name").toString();
```

```python
# [Python] @Property 装饰器
from PySide6.QtCore import QObject, Property, Signal

class Person(QObject):
    nameChanged = Signal(str)
    ageChanged = Signal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._name = ""
        self._age = 0
    
    def _get_name(self):
        return self._name
    
    def _set_name(self, name):
        if self._name != name:
            self._name = name
            self.nameChanged.emit(name)
    
    name = Property(str, _get_name, _set_name, notify=nameChanged)
    
    def _get_age(self):
        return self._age
    
    def _set_age(self, age):
        if self._age != age:
            self._age = age
            self.ageChanged.emit(age)
    
    age = Property(int, _get_age, _set_age, notify=ageChanged)

# 使用
person = Person()
person.setProperty("name", "Alice")
name = person.property("name")
```

---

## 3.4 容器类（Container Classes）

Qt 提供了丰富的容器类，与 STL 容器类似但提供了更好的 Qt 集成。

### 3.4.1 顺序容器

```cpp
// [C++] QList, QVector, QStack, QQueue
#include <QList>
#include <QVector>
#include <QStack>
#include <QQueue>

// QList - 通用列表
QList<int> numbers;
numbers << 1 << 2 << 3;
numbers.append(4);
numbers.prepend(0);

for (int num : numbers) {
    qDebug() << num;
}

// QVector - 连续存储，随机访问快
QVector<double> values = {1.1, 2.2, 3.3};
double first = values.first();
double last = values.last();

// QStack - 栈
QStack<QString> stack;
stack.push("first");
stack.push("second");
QString top = stack.pop();  // "second"

// QQueue - 队列
QQueue<int> queue;
queue.enqueue(1);
queue.enqueue(2);
int front = queue.dequeue();  // 1
```

```python
# [Python] 使用 Python 原生容器
# Python 中通常直接使用 list, dict 等原生类型
# PySide6 会自动处理类型转换

# 列表
numbers = [1, 2, 3, 4]
numbers.append(5)
numbers.insert(0, 0)

# 字典
person = {"name": "Alice", "age": 30}
name = person["name"]

# 但在某些情况下需要使用 Qt 容器
from PySide6.QtCore import QStringList

string_list = QStringList()
string_list << "Apple" << "Banana" << "Cherry"
```

### 3.4.2 关联容器

```cpp
// [C++] QMap, QHash, QSet
#include <QMap>
#include <QHash>
#include <QSet>

// QMap - 有序映射（按键排序）
QMap<QString, int> scores;
scores["Alice"] = 95;
scores["Bob"] = 87;
scores["Charlie"] = 92;

for (auto it = scores.begin(); it != scores.end(); ++it) {
    qDebug() << it.key() << ":" << it.value();
}

// QHash - 哈希表，查找更快
QHash<QString, QString> phoneBook;
phoneBook["Alice"] = "123-4567";
phoneBook["Bob"] = "987-6543";

// QSet - 集合
QSet<int> set1 = {1, 2, 3};
QSet<int> set2 = {3, 4, 5};
QSet<int> intersection = set1 & set2;  // {3}
QSet<int> union_ = set1 | set2;        // {1, 2, 3, 4, 5}
```

### 3.4.3 QVariant - 通用值容器

```cpp
// [C++] QVariant 可以存储任何 Qt 类型
#include <QVariant>

QVariant var;

var = 42;  // 存储 int
int i = var.toInt();

var = "Hello";  // 存储 QString
QString s = var.toString();

var = 3.14;  // 存储 double
double d = var.toDouble();

// 检查类型
if (var.typeId() == QMetaType::Double) {
    qDebug() << "It's a double";
}
```

```python
# [Python] QVariant 自动处理
# Python 中 QVariant 通常由 PySide6 自动处理
# 但也可以显式使用

from PySide6.QtCore import QVariant

var = QVariant(42)
value = var.toInt()

var = QVariant("Hello")
string = var.toString()
```

---

## 3.5 I/O 系统

Qt 提供了强大的 I/O 系统，包括文件、目录、数据流等。

### 3.5.1 文件操作

```cpp
// [C++] 文件读写
#include <QFile>
#include <QTextStream>
#include <QDataStream>
#include <QDebug>

// 文本文件写入
QFile file("data.txt");
if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
    QTextStream stream(&file);
    stream << "Hello, Qt!\n";
    stream << "Line 2\n";
    file.close();
}

// 文本文件读取
if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    QTextStream stream(&file);
    while (!stream.atEnd()) {
        QString line = stream.readLine();
        qDebug() << line;
    }
    file.close();
}

// 二进制文件
QFile binFile("data.bin");
if (binFile.open(QIODevice::WriteOnly)) {
    QDataStream stream(&binFile);
    stream << QString("Binary data") << 42 << 3.14;
    binFile.close();
}
```

```python
# [Python] 文件操作
from PySide6.QtCore import QFile, QTextStream, QDataStream, QIODevice

# 文本文件写入
file = QFile("data.txt")
if file.open(QIODevice.WriteOnly | QIODevice.Text):
    stream = QTextStream(file)
    stream << "Hello, Qt!\n"
    stream << "Line 2\n"
    file.close()

# 也可以使用 Python 原生方式
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("Hello, Python!\n")
```

### 3.5.2 目录操作

```cpp
// [C++] 目录操作
#include <QDir>
#include <QFileInfo>

QDir dir("/path/to/directory");

// 检查目录是否存在
if (dir.exists()) {
    // 列出所有文件
    QStringList files = dir.entryList(QDir::Files);
    for (const QString &file : files) {
        qDebug() << file;
    }
    
    // 递归列出
    QStringList allFiles = dir.entryList(QDir::Files | QDir::NoDotAndDotDot, 
                                          QDir::Name | QDir::Reversed);
}

// 创建目录
QDir().mkpath("path/to/new/directory");

// 获取文件信息
QFileInfo info("file.txt");
qDebug() << "Size:" << info.size();
qDebug() << "Created:" << info.birthTime();
qDebug() << "Modified:" << info.lastModified();
```

---

## 3.6 事件循环（Event Loop）

Qt 使用事件循环处理异步事件，是 GUI 应用的核心机制。

### 3.6.1 基础事件循环

```cpp
// [C++] QCoreApplication 事件循环
#include <QCoreApplication>
#include <QTimer>
#include <QDebug>

int main(int argc, char *argv[])
{
    QCoreApplication app(argc, argv);
    
    // 使用定时器在事件循环中执行任务
    QTimer::singleShot(1000, [&]() {
        qDebug() << "1 second passed";
        app.quit();  // 退出事件循环
    });
    
    qDebug() << "Starting event loop...";
    return app.exec();  // 进入事件循环
}
```

```python
# [Python] 事件循环
from PySide6.QtCore import QCoreApplication, QTimer

app = QCoreApplication([])

def on_timeout():
    print("1 second passed")
    app.quit()

QTimer.singleShot(1000, on_timeout)

print("Starting event loop...")
app.exec()
```

### 3.6.2 自定义事件

```cpp
// [C++] 自定义事件
#include <QEvent>
#include <QCoreApplication>

const QEvent::Type MyCustomEventType = static_cast<QEvent::Type>(QEvent::User + 1);

class MyCustomEvent : public QEvent
{
public:
    MyCustomEvent(const QString &data) 
        : QEvent(MyCustomEventType), m_data(data) {}
    
    QString data() const { return m_data; }
    
private:
    QString m_data;
};

class MyObject : public QObject
{
protected:
    bool event(QEvent *event) override {
        if (event->type() == MyCustomEventType) {
            MyCustomEvent *customEvent = static_cast<MyCustomEvent*>(event);
            qDebug() << "Custom event received:" << customEvent->data();
            return true;
        }
        return QObject::event(event);
    }
};

// 发送自定义事件
MyObject obj;
QCoreApplication::postEvent(&obj, new MyCustomEvent("Hello Event"));
```

---

## 3.7 多线程（Threading）

Qt 提供了多种多线程编程方式。

### 3.7.1 QThread 基础

```cpp
// [C++] 使用 QThread
#include <QThread>
#include <QDebug>

class Worker : public QObject
{
    Q_OBJECT
public slots:
    void doWork() {
        qDebug() << "Working in thread:" << QThread::currentThreadId();
        // 耗时操作
        QThread::sleep(2);
        emit workFinished();
    }
signals:
    void workFinished();
};

// 使用
QThread thread;
Worker worker;
worker.moveToThread(&thread);

QObject::connect(&thread, &QThread::started, &worker, &Worker::doWork);
QObject::connect(&worker, &Worker::workFinished, &thread, &QThread::quit);
QObject::connect(&worker, &Worker::workFinished, &worker, &Worker::deleteLater);
QObject::connect(&thread, &QThread::finished, &thread, &QThread::deleteLater);

thread.start();
```

```python
# [Python] QThread
from PySide6.QtCore import QThread, QObject, Signal, Slot
import time

class Worker(QObject):
    workFinished = Signal()
    
    @Slot()
    def doWork(self):
        print(f"Working in thread: {QThread.currentThreadId()}")
        time.sleep(2)
        self.workFinished.emit()

# 使用
thread = QThread()
worker = Worker()
worker.moveToThread(thread)

thread.started.connect(worker.doWork)
worker.workFinished.connect(thread.quit)
worker.workFinished.connect(worker.deleteLater)
thread.finished.connect(thread.deleteLater)

thread.start()
```

### 3.7.2 线程同步

```cpp
// [C++] 线程同步原语
#include <QMutex>
#include <QMutexLocker>
#include <QReadWriteLock>
#include <QSemaphore>
#include <QWaitCondition>

// QMutex - 互斥锁
QMutex mutex;
int sharedData = 0;

void threadSafeFunction() {
    QMutexLocker locker(&mutex);  // 自动加锁/解锁
    ++sharedData;
}  // 离开作用域自动解锁

// QReadWriteLock - 读写锁
QReadWriteLock rwLock;
QString sharedString;

void readData() {
    QReadLocker locker(&rwLock);
    // 多个线程可同时读取
    qDebug() << sharedString;
}

void writeData(const QString &data) {
    QWriteLocker locker(&rwLock);
    // 独占写访问
    sharedString = data;
}
```

---

## 3.8 定时器（Timer）

Qt 提供了灵活的定时器机制。

### 3.8.1 QTimer 使用

```cpp
// [C++] QTimer
#include <QTimer>
#include <QDebug>

// 方法1：单次定时器
QTimer::singleShot(1000, []() {
    qDebug() << "One shot timer fired!";
});

// 方法2：重复定时器
QTimer *timer = new QTimer();
QObject::connect(timer, &QTimer::timeout, []() {
    qDebug() << "Timer tick!" << QDateTime::currentDateTime();
});
timer->start(1000);  // 每秒触发一次

// 停止定时器
timer->stop();
```

```python
# [Python] QTimer
from PySide6.QtCore import QTimer, QDateTime

# 单次定时器
QTimer.singleShot(1000, lambda: print("One shot timer fired!"))

# 重复定时器
timer = QTimer()
timer.timeout.connect(lambda: print(f"Timer tick! {QDateTime.currentDateTime()}"))
timer.start(1000)  # 每秒触发一次

# 停止
timer.stop()
```

### 3.8.2 高精度定时器

```cpp
// [C++] QElapsedTimer - 测量时间间隔
#include <QElapsedTimer>
#include <QDebug>

QElapsedTimer timer;
timer.start();

// 执行一些操作...
for (int i = 0; i < 1000000; ++i) {
    // some work
}

qint64 elapsed = timer.elapsed();  // 毫秒
qint64 nano = timer.nsecsElapsed();  // 纳秒
qDebug() << "Elapsed:" << elapsed << "ms";
```

---

## 3.9 本章小结

本章介绍了 Qt Core 的核心功能：

| 主题 | 关键类 | 主要用途 |
|------|--------|----------|
| 元对象系统 | `QObject`, `QMetaObject` | 运行时类型信息、对象树 |
| 信号与槽 | `Signal`, `Slot` | 对象间通信 |
| 属性系统 | `Q_PROPERTY`, `Property` | 动态属性访问 |
| 容器 | `QList`, `QMap`, `QVariant` | 数据存储 |
| I/O | `QFile`, `QDir`, `QTextStream` | 文件操作 |
| 事件循环 | `QCoreApplication`, `QEvent` | 异步处理 |
| 多线程 | `QThread`, `QMutex` | 并发编程 |
| 定时器 | `QTimer`, `QElapsedTimer` | 定时任务 |

这些核心概念是理解 Qt 其他模块的基础。在下一章中，我们将探索 Qt GUI 模块，学习 2D 绘图、图像处理和事件处理。
