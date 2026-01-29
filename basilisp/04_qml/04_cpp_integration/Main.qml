/**
 * QML 与 C++ 集成示例
 *
 * 展示：
 * - 使用 C++ 类型创建对象
 * - 访问 C++ 属性
 * - 调用 C++ 方法
 * - 处理 C++ 信号
 */

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QmlCppIntegration 1.0  // 导入模块 (包含 Counter)

ApplicationWindow {
    id: root
    width: 450
    height: 500
    visible: true
    title: "QML + C++ 集成"

    // 方式1: 使用 QML_ELEMENT 注册的类型创建实例
    Counter {
        id: localCounter
        step: stepSlider.value

        // 处理 C++ 信号
        onValueChanged: {
            console.log("[QML] 值变化:", value)
        }

        onLimitReached: (message) => {
            statusLabel.text = message
            statusLabel.color = "red"
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        Label {
            text: "QML + C++ 集成示例"
            font.pixelSize: 22
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
        }

        // 显示上下文属性
        Label {
            text: "应用版本: " + appVersion + (debugMode ? " (调试模式)" : "")
            color: "#666"
            Layout.alignment: Qt.AlignHCenter
        }

        Rectangle {
            Layout.fillWidth: true
            height: 2
            color: "#ddd"
        }

        // 本地 Counter 实例
        GroupBox {
            title: "本地 Counter 实例 (QML_ELEMENT)"
            Layout.fillWidth: true

            ColumnLayout {
                width: parent.width

                // 显示 C++ 属性
                Label {
                    text: localCounter.displayText  // 使用 C++ 只读属性
                    font.pixelSize: 24
                    font.bold: true
                    Layout.alignment: Qt.AlignHCenter
                }

                // 进度条绑定到 C++ 属性
                ProgressBar {
                    Layout.fillWidth: true
                    from: 0
                    to: 100
                    value: localCounter.value
                }

                // 步长控制
                RowLayout {
                    Label { text: "步长:" }
                    Slider {
                        id: stepSlider
                        Layout.fillWidth: true
                        from: 1
                        to: 10
                        value: 1
                        stepSize: 1
                    }
                    Label { text: stepSlider.value }
                }

                // 调用 C++ 方法
                RowLayout {
                    Layout.alignment: Qt.AlignHCenter

                    Button {
                        text: "-"
                        onClicked: localCounter.decrement()  // 调用 Q_INVOKABLE
                    }

                    Button {
                        text: "重置"
                        onClicked: localCounter.reset()
                    }

                    Button {
                        text: "+"
                        onClicked: localCounter.increment()
                    }
                }

                // 直接设置 C++ 属性
                RowLayout {
                    Label { text: "直接设置值:" }
                    Slider {
                        Layout.fillWidth: true
                        from: 0
                        to: 100
                        value: localCounter.value
                        onMoved: localCounter.value = value  // 设置 C++ 属性
                    }
                }

                // 调用带返回值的 C++ 方法
                Button {
                    text: "格式化显示"
                    onClicked: {
                        var result = localCounter.formatValue("计数器")
                        formattedLabel.text = result
                    }
                }
                Label {
                    id: formattedLabel
                    text: "-"
                    color: "#666"
                }
            }
        }

        // 全局 Counter 实例 (上下文属性)
        GroupBox {
            title: "全局 Counter 实例 (Context Property)"
            Layout.fillWidth: true

            ColumnLayout {
                width: parent.width

                Label {
                    text: globalCounter.displayText
                    font.pixelSize: 18
                }

                RowLayout {
                    Button {
                        text: "-"
                        onClicked: globalCounter.decrement()
                    }
                    Button {
                        text: "+"
                        onClicked: globalCounter.increment()
                    }

                    Label {
                        text: "值: " + globalCounter.value
                    }
                }
            }
        }

        // 状态显示
        Label {
            id: statusLabel
            text: "就绪"
            color: "#666"
            Layout.alignment: Qt.AlignHCenter

            // 自动恢复
            onTextChanged: {
                if (color === "red") {
                    statusResetTimer.restart()
                }
            }
        }

        Timer {
            id: statusResetTimer
            interval: 2000
            onTriggered: {
                statusLabel.text = "就绪"
                statusLabel.color = "#666"
            }
        }

        Item { Layout.fillHeight: true }

        // 说明
        Label {
            text: "C++ 类通过 QML_ELEMENT 注册后可在 QML 中直接使用"
            wrapMode: Text.Wrap
            font.italic: true
            color: "#888"
            Layout.fillWidth: true
        }
    }
}
