/**
 * Qt Quick Visual Effects 示例
 *
 * 展示内容：
 * - Opacity: 透明度
 * - Rotation: 旋转
 * - Scale: 缩放
 * - Animation: 动画效果
 * - Gradient: 渐变效果
 * - Shadow: 阴影效果（使用内嵌矩形模拟）
 */

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 600
    height: 800
    visible: true
    title: "Qt Quick Visual Effects"

    ScrollView {
        anchors.fill: parent

        ColumnLayout {
            width: root.width - 40
            x: 20
            spacing: 15

            Label {
                text: "Visual Effects 视觉效果"
                font.pixelSize: 24
                font.bold: true
                Layout.topMargin: 20
            }

            // 1. Opacity 透明度
            GroupBox {
                title: "1. Opacity (透明度)"
                Layout.fillWidth: true

                Column {
                    spacing: 10
                    width: parent.width

                    Slider {
                        id: opacitySlider
                        width: parent.width
                        from: 0
                        to: 1
                        value: 1
                    }

                    Row {
                        spacing: 15

                        Rectangle {
                            width: 80
                            height: 80
                            color: "red"
                            opacity: opacitySlider.value
                            radius: 10

                            Text {
                                anchors.centerIn: parent
                                text: Math.round(opacitySlider.value * 100) + "%"
                                color: "white"
                                font.bold: true
                            }
                        }

                        Rectangle {
                            width: 80
                            height: 80
                            color: "green"
                            opacity: opacitySlider.value
                            radius: 40
                        }

                        Rectangle {
                            width: 80
                            height: 80
                            gradient: Gradient {
                                GradientStop { position: 0; color: "blue" }
                                GradientStop { position: 1; color: "cyan" }
                            }
                            opacity: opacitySlider.value
                            radius: 10
                        }
                    }
                }
            }

            // 2. Rotation 旋转
            GroupBox {
                title: "2. Rotation (旋转)"
                Layout.fillWidth: true

                Column {
                    spacing: 10
                    width: parent.width

                    Slider {
                        id: rotationSlider
                        width: parent.width
                        from: 0
                        to: 360
                        value: 0
                    }

                    Row {
                        spacing: 30

                        Rectangle {
                            width: 80
                            height: 80
                            color: "coral"
                            radius: 10
                            rotation: rotationSlider.value

                            Text {
                                anchors.centerIn: parent
                                text: rotationSlider.value.toFixed(0) + "°"
                                font.bold: true
                            }
                        }

                        Rectangle {
                            width: 80
                            height: 80
                            color: "transparent"
                            border.color: "steelblue"
                            border.width: 4
                            rotation: rotationSlider.value

                            // 围绕中心旋转
                            transformOrigin: Item.Center
                        }

                        Rectangle {
                            width: 80
                            height: 80
                            gradient: Gradient {
                                GradientStop { position: 0; color: "purple" }
                                GradientStop { position: 1; color: "pink" }
                            }
                            rotation: -rotationSlider.value * 2  // 反向双倍速度
                        }
                    }

                    Label {
                        text: "拖动滑块旋转元素"
                        font.pixelSize: 12
                        color: "gray"
                    }
                }
            }

            // 3. Scale 缩放
            GroupBox {
                title: "3. Scale (缩放)"
                Layout.fillWidth: true

                Column {
                    spacing: 10
                    width: parent.width

                    Slider {
                        id: scaleSlider
                        width: parent.width
                        from: 0.5
                        to: 2
                        value: 1
                    }

                    Row {
                        spacing: 30
                        height: 100
                        anchors.horizontalCenter: parent.horizontalCenter

                        Rectangle {
                            anchors.verticalCenter: parent.verticalCenter
                            width: 60
                            height: 60
                            color: "gold"
                            scale: scaleSlider.value
                            radius: 10

                            Text {
                                anchors.centerIn: parent
                                text: (scaleSlider.value).toFixed(1) + "x"
                                font.bold: true
                                scale: 1 / scaleSlider.value  // 保持文字大小不变
                            }
                        }

                        Rectangle {
                            anchors.verticalCenter: parent.verticalCenter
                            width: 60
                            height: 60
                            color: "lightseagreen"
                            scale: scaleSlider.value
                            radius: 30
                        }
                    }
                }
            }

            // 4. DropShadow 阴影效果（使用偏移矩形模拟）
            GroupBox {
                title: "4. DropShadow (阴影 - 模拟效果)"
                Layout.fillWidth: true

                Column {
                    spacing: 15
                    width: parent.width

                    Row {
                        spacing: 25

                        // 带阴影的矩形（使用底层矩形模拟阴影）
                        Item {
                            width: 100
                            height: 60

                            // 阴影层
                            Rectangle {
                                width: 100
                                height: 60
                                color: "#80000000"
                                radius: 10
                                x: 4
                                y: 4
                            }

                            // 主体
                            Rectangle {
                                width: 100
                                height: 60
                                color: "white"
                                radius: 10

                                Text {
                                    anchors.centerIn: parent
                                    text: "阴影效果"
                                }
                            }
                        }

                        // 发光效果（使用边框模拟）
                        Rectangle {
                            width: 60
                            height: 60
                            radius: 30
                            color: "orange"
                            border.color: "#FFFFA500"
                            border.width: 4
                            opacity: 0.9

                            // 外层光晕
                            Rectangle {
                                anchors.centerIn: parent
                                width: 70
                                height: 70
                                radius: 35
                                color: "transparent"
                                border.color: "#60FFA500"
                                border.width: 2
                            }
                        }

                        // 卡片效果
                        Item {
                            width: 100
                            height: 70

                            Rectangle {
                                width: 100
                                height: 70
                                color: "#20000000"
                                radius: 8
                                x: 0
                                y: 2
                            }

                            Rectangle {
                                width: 100
                                height: 70
                                color: "white"
                                radius: 8

                                Column {
                                    anchors.centerIn: parent
                                    spacing: 5

                                    Rectangle {
                                        width: 60
                                        height: 8
                                        color: "#ddd"
                                        radius: 4
                                        anchors.horizontalCenter: parent.horizontalCenter
                                    }
                                    Rectangle {
                                        width: 40
                                        height: 8
                                        color: "#ddd"
                                        radius: 4
                                        anchors.horizontalCenter: parent.horizontalCenter
                                    }
                                }
                            }
                        }
                    }
                }
            }

            // 5. 组合效果
            GroupBox {
                title: "5. 组合效果 (Rotation + Scale + Opacity)"
                Layout.fillWidth: true

                Rectangle {
                    width: parent.width
                    height: 150
                    color: "#f5f5f5"

                    Rectangle {
                        id: comboRect
                        width: 80
                        height: 80
                        color: "dodgerblue"
                        radius: 10
                        anchors.centerIn: parent

                        Text {
                            anchors.centerIn: parent
                            text: "动画中"
                            color: "white"
                            font.bold: true
                        }

                        // 动画: 旋转 + 缩放 + 透明度变化
                        SequentialAnimation on rotation {
                            loops: Animation.Infinite
                            NumberAnimation {
                                from: 0
                                to: 360
                                duration: 2000
                                easing.type: Easing.Linear
                            }
                        }

                        SequentialAnimation on scale {
                            loops: Animation.Infinite
                            NumberAnimation {
                                from: 1
                                to: 1.3
                                duration: 1000
                                easing.type: Easing.InOutQuad
                            }
                            NumberAnimation {
                                from: 1.3
                                to: 1
                                duration: 1000
                                easing.type: Easing.InOutQuad
                            }
                        }

                        SequentialAnimation on opacity {
                            loops: Animation.Infinite
                            NumberAnimation {
                                from: 1
                                to: 0.5
                                duration: 1000
                            }
                            NumberAnimation {
                                from: 0.5
                                to: 1
                                duration: 1000
                            }
                        }
                    }
                }
            }

            // 6. 渐变效果
            GroupBox {
                title: "6. Gradient (渐变效果)"
                Layout.fillWidth: true

                Column {
                    spacing: 10
                    width: parent.width

                    Row {
                        spacing: 15
                        anchors.horizontalCenter: parent.horizontalCenter

                        // 线性渐变
                        Rectangle {
                            width: 100
                            height: 60
                            radius: 8
                            gradient: Gradient {
                                orientation: Gradient.Horizontal
                                GradientStop { position: 0; color: "red" }
                                GradientStop { position: 0.5; color: "yellow" }
                                GradientStop { position: 1; color: "green" }
                            }

                            Text {
                                anchors.centerIn: parent
                                text: "水平渐变"
                                color: "white"
                                font.bold: true
                            }
                        }

                        // 垂直渐变
                        Rectangle {
                            width: 100
                            height: 60
                            radius: 8
                            gradient: Gradient {
                                GradientStop { position: 0; color: "blue" }
                                GradientStop { position: 1; color: "cyan" }
                            }

                            Text {
                                anchors.centerIn: parent
                                text: "垂直渐变"
                                color: "white"
                                font.bold: true
                            }
                        }

                        // 对角渐变（使用角度）
                        Rectangle {
                            width: 60
                            height: 60
                            radius: 30
                            gradient: Gradient {
                                GradientStop { position: 0; color: "purple" }
                                GradientStop { position: 1; color: "pink" }
                            }

                            Text {
                                anchors.centerIn: parent
                                text: "圆形"
                                color: "white"
                                font.bold: true
                                font.pixelSize: 10
                            }
                        }
                    }
                }
            }

            // 7. 颜色调整（使用 opacity 和 overlay 模拟）
            GroupBox {
                title: "7. 颜色调整 (Brightness/Contrast 模拟)"
                Layout.fillWidth: true

                Column {
                    spacing: 10
                    width: parent.width

                    Row {
                        spacing: 10

                        Column {
                            Label { text: "亮度模拟" }
                            Slider {
                                id: brightnessSlider
                                width: 150
                                from: 0
                                to: 1
                                value: 0.5
                            }
                        }

                        Column {
                            Label { text: "叠加色" }
                            ComboBox {
                                id: overlayColor
                                width: 120
                                model: ["白色", "黑色", "红色", "蓝色"]
                            }
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 80
                        color: "#f0f0f0"

                        Row {
                            anchors.centerIn: parent
                            spacing: 20

                            // 原图
                            Rectangle {
                                width: 60
                                height: 60
                                color: "teal"
                                radius: 5

                                Text {
                                    anchors.centerIn: parent
                                    text: "原图"
                                    color: "white"
                                }
                            }

                            // 调整后的（使用半透明叠加层模拟亮度调整）
                            Rectangle {
                                width: 60
                                height: 60
                                color: "teal"
                                radius: 5

                                Rectangle {
                                    anchors.fill: parent
                                    color: {
                                        switch(overlayColor.currentIndex) {
                                            case 0: return "#FFFFFF"
                                            case 1: return "#000000"
                                            case 2: return "#FF0000"
                                            case 3: return "#0000FF"
                                            default: return "#FFFFFF"
                                        }
                                    }
                                    opacity: brightnessSlider.value
                                    radius: 5
                                }

                                Text {
                                    anchors.centerIn: parent
                                    text: "调整后"
                                    color: "white"
                                }
                            }

                            // 另一个示例
                            Rectangle {
                                width: 60
                                height: 60
                                gradient: Gradient {
                                    GradientStop { position: 0; color: "orange" }
                                    GradientStop { position: 1; color: "red" }
                                }
                                radius: 5

                                Rectangle {
                                    anchors.fill: parent
                                    color: "white"
                                    opacity: 1 - brightnessSlider.value
                                    radius: 5
                                }
                            }
                        }
                    }
                }
            }

            Item { height: 20 }
        }
    }
}
