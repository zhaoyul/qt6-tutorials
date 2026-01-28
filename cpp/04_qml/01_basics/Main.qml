/**
 * QML 基础语法示例
 *
 * 主要概念：
 * - 元素层次结构
 * - 属性声明和绑定
 * - JavaScript 函数
 * - 信号处理
 */

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 500
    height: 600
    visible: true
    title: "Qt6 QML Basics"

    // 自定义属性
    property int clickCount: 0
    property color themeColor: "#3498db"

    // JavaScript 函数
    function incrementCounter() {
        clickCount++
        console.log("点击次数:", clickCount)
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        // 标题
        Label {
            text: "QML 基础示例"
            font.pixelSize: 24
            font.bold: true
            color: root.themeColor
            Layout.alignment: Qt.AlignHCenter
        }

        // 分隔线
        Rectangle {
            Layout.fillWidth: true
            height: 2
            color: "#ddd"
        }

        // 1. 基础元素
        GroupBox {
            title: "1. 基础元素"
            Layout.fillWidth: true

            RowLayout {
                spacing: 20

                // 矩形
                Rectangle {
                    width: 60; height: 60
                    color: "coral"
                    radius: 10

                    // 鼠标交互
                    MouseArea {
                        anchors.fill: parent
                        onClicked: parent.color = Qt.rgba(Math.random(), Math.random(), Math.random(), 1)
                    }
                }

                // 文本
                Text {
                    text: "Hello QML!"
                    font.pixelSize: 18
                    color: "#333"
                }

                // 图像占位
                Rectangle {
                    width: 60; height: 60
                    color: "#f0f0f0"
                    border.color: "#ccc"

                    Text {
                        anchors.centerIn: parent
                        text: "Image\nPlaceholder"
                        font.pixelSize: 10
                        horizontalAlignment: Text.AlignHCenter
                    }
                }
            }
        }

        // 2. 属性绑定
        GroupBox {
            title: "2. 属性绑定"
            Layout.fillWidth: true

            ColumnLayout {
                width: parent.width

                Slider {
                    id: sizeSlider
                    Layout.fillWidth: true
                    from: 20
                    to: 100
                    value: 50
                }

                Rectangle {
                    // 属性绑定：自动随滑块变化
                    width: sizeSlider.value
                    height: sizeSlider.value
                    color: root.themeColor
                    radius: sizeSlider.value / 4

                    Text {
                        anchors.centerIn: parent
                        text: Math.round(sizeSlider.value)
                        color: "white"
                        font.bold: true
                    }
                }

                Label {
                    text: "滑块值自动绑定到矩形大小"
                    font.italic: true
                    color: "#666"
                }
            }
        }

        // 3. 信号和处理器
        GroupBox {
            title: "3. 信号和处理器"
            Layout.fillWidth: true

            RowLayout {
                Button {
                    text: "点击计数: " + root.clickCount

                    // 信号处理器
                    onClicked: root.incrementCounter()
                }

                Button {
                    text: "重置"
                    onClicked: root.clickCount = 0
                }

                // 自定义信号示例
                Item {
                    id: signalExample
                    signal customSignal(string message)

                    onCustomSignal: (message) => {
                        console.log("收到自定义信号:", message)
                    }
                }

                Button {
                    text: "发送信号"
                    onClicked: signalExample.customSignal("Hello from QML!")
                }
            }
        }

        // 4. JavaScript 集成
        GroupBox {
            title: "4. JavaScript 集成"
            Layout.fillWidth: true

            ColumnLayout {
                width: parent.width

                TextField {
                    id: inputField
                    Layout.fillWidth: true
                    placeholderText: "输入文字..."
                }

                Label {
                    // JavaScript 表达式
                    text: "字符数: " + inputField.text.length +
                          " | 大写: " + inputField.text.toUpperCase()
                    wrapMode: Text.Wrap
                }

                Button {
                    text: "计算随机数"
                    onClicked: {
                        // 内联 JavaScript
                        var random = Math.floor(Math.random() * 100)
                        resultLabel.text = "随机数: " + random
                    }
                }

                Label {
                    id: resultLabel
                    text: "随机数: -"
                }
            }
        }

        // 5. 定位器
        GroupBox {
            title: "5. 定位器 (Row, Column, Grid)"
            Layout.fillWidth: true

            Row {
                spacing: 20

                Column {
                    spacing: 5
                    Repeater {
                        model: 3
                        Rectangle {
                            width: 40; height: 25
                            color: Qt.hsla(index * 0.1, 0.7, 0.5, 1)
                            Text {
                                anchors.centerIn: parent
                                text: index + 1
                                color: "white"
                            }
                        }
                    }
                }

                Grid {
                    columns: 3
                    spacing: 3
                    Repeater {
                        model: 9
                        Rectangle {
                            width: 25; height: 25
                            color: Qt.hsla(index * 0.04, 0.7, 0.5, 1)
                            Text {
                                anchors.centerIn: parent
                                text: index + 1
                                color: "white"
                                font.pixelSize: 10
                            }
                        }
                    }
                }

                Flow {
                    width: 100
                    spacing: 3
                    Repeater {
                        model: 6
                        Rectangle {
                            width: 30; height: 20
                            color: Qt.hsla(0.5 + index * 0.05, 0.7, 0.5, 1)
                        }
                    }
                }
            }
        }

        // 填充剩余空间
        Item { Layout.fillHeight: true }

        // 底部说明
        Label {
            text: "QML 提供声明式 UI 定义，属性绑定使 UI 自动响应数据变化"
            wrapMode: Text.Wrap
            font.italic: true
            color: "#666"
            Layout.fillWidth: true
        }
    }
}
