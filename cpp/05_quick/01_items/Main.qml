/**
 * Qt Quick 基础元素示例
 *
 * 展示内容：
 * - Rectangle: 矩形元素
 * - Text: 文本元素
 * - Image: 图像元素
 * - MouseArea: 鼠标交互区域
 */

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 600
    height: 700
    visible: true
    title: "Qt Quick Basic Items"

    ScrollView {
        anchors.fill: parent

        ColumnLayout {
            width: root.width - 40
            x: 20
            spacing: 15

            Label {
                text: "Qt Quick 基础元素"
                font.pixelSize: 24
                font.bold: true
                Layout.topMargin: 20
            }

            // 1. Rectangle 矩形
            GroupBox {
                title: "1. Rectangle (矩形)"
                Layout.fillWidth: true

                Column {
                    spacing: 10

                    // 基础矩形
                    Rectangle {
                        width: 200
                        height: 60
                        color: "steelblue"
                        radius: 10
                    }

                    // 渐变矩形
                    Rectangle {
                        width: 200
                        height: 60
                        radius: 10
                        gradient: Gradient {
                            GradientStop { position: 0.0; color: "lightcoral" }
                            GradientStop { position: 1.0; color: "darkred" }
                        }
                    }

                    // 带边框的矩形
                    Rectangle {
                        width: 200
                        height: 60
                        color: "lightgreen"
                        border.color: "darkgreen"
                        border.width: 3
                        radius: 15
                    }
                }
            }

            // 2. Text 文本
            GroupBox {
                title: "2. Text (文本)"
                Layout.fillWidth: true

                Column {
                    spacing: 10

                    Text {
                        text: "普通文本"
                        font.pixelSize: 16
                    }

                    Text {
                        text: "粗体文本"
                        font.pixelSize: 16
                        font.bold: true
                        color: "navy"
                    }

                    Text {
                        text: "斜体带下划线"
                        font.pixelSize: 16
                        font.italic: true
                        font.underline: true
                        color: "darkgreen"
                    }

                    Text {
                        text: "带阴影的文本"
                        font.pixelSize: 20
                        font.bold: true
                        color: "white"
                        style: Text.Raised
                        styleColor: "black"
                    }

                    Text {
                        width: 200
                        text: "这是一段很长的文本，设置了 wrapMode 属性后会自动换行显示"
                        wrapMode: Text.WordWrap
                        font.pixelSize: 14
                    }
                }
            }

            // 3. MouseArea 鼠标交互
            GroupBox {
                title: "3. MouseArea (鼠标交互)"
                Layout.fillWidth: true

                Column {
                    spacing: 10

                    Rectangle {
                        id: clickRect
                        width: 200
                        height: 60
                        color: mouseArea.pressed ? "darkorange" : "orange"
                        radius: 10

                        Text {
                            anchors.centerIn: parent
                            text: mouseArea.containsMouse ? "鼠标悬停" : "点击我"
                            color: "white"
                            font.bold: true
                        }

                        MouseArea {
                            id: mouseArea
                            anchors.fill: parent
                            hoverEnabled: true
                            onClicked: console.log("矩形被点击!")
                            onDoubleClicked: console.log("矩形被双击!")
                        }
                    }

                    // 拖拽示例
                    Rectangle {
                        width: 250
                        height: 80
                        color: "#f0f0f0"
                        border.color: "#ccc"

                        Rectangle {
                            id: draggableRect
                            width: 50
                            height: 50
                            color: "purple"
                            radius: 25
                            x: 10
                            y: 15

                            Text {
                                anchors.centerIn: parent
                                text: "拖我"
                                color: "white"
                                font.pixelSize: 10
                            }

                            MouseArea {
                                anchors.fill: parent
                                drag.target: draggableRect
                                drag.axis: Drag.XAndYAxis
                                drag.minimumX: 0
                                drag.maximumX: 200
                                drag.minimumY: 0
                                drag.maximumY: 30
                            }
                        }
                    }
                }
            }

            // 4. Image 图像
            GroupBox {
                title: "4. Image (图像)"
                Layout.fillWidth: true

                Column {
                    spacing: 10

                    Row {
                        spacing: 20

                        // 纯色作为占位图像
                        Rectangle {
                            width: 80
                            height: 80
                            color: "lightblue"
                            border.color: "blue"
                            border.width: 2

                            Text {
                                anchors.centerIn: parent
                                text: "Image\n占位"
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }

                        // 带圆角的图像占位
                        Rectangle {
                            width: 80
                            height: 80
                            radius: 40
                            color: "lightcoral"
                            clip: true

                            Text {
                                anchors.centerIn: parent
                                text: "圆形\n裁剪"
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }

                        // 旋转的图像占位
                        Rectangle {
                            width: 80
                            height: 80
                            color: "lightgreen"
                            rotation: 45

                            Text {
                                anchors.centerIn: parent
                                text: "旋转"
                                rotation: -45
                            }
                        }
                    }

                    Label {
                        text: "提示: Image 元素支持本地文件和网络图片"
                        font.pixelSize: 12
                        color: "gray"
                    }
                }
            }

            // 5. 综合示例
            GroupBox {
                title: "5. 综合示例 - 按钮"
                Layout.fillWidth: true

                Column {
                    spacing: 10

                    Rectangle {
                        id: customButton
                        width: 150
                        height: 40
                        color: mouseArea2.pressed ? "darkgreen" : "seagreen"
                        radius: 8

                        Text {
                            anchors.centerIn: parent
                            text: "自定义按钮"
                            color: "white"
                            font.bold: true
                        }

                        MouseArea {
                            id: mouseArea2
                            anchors.fill: parent
                            onClicked: console.log("自定义按钮被点击!")
                        }
                    }
                }
            }

            Item { height: 20 }
        }
    }
}
