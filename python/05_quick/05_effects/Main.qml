/**
 * Qt Quick Visual Effects 示例
 *
 * 展示内容：
 * - Opacity: 透明度
 * - Rotation: 旋转
 * - Scale: 缩放
 * - ShaderEffect: 着色器效果
 * - Blend: 混合模式
 * - DropShadow: 阴影效果
 */

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

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

            // 4. DropShadow 阴影效果
            GroupBox {
                title: "4. DropShadow (阴影)"
                Layout.fillWidth: true

                Column {
                    spacing: 15
                    width: parent.width

                    Row {
                        spacing: 20

                        // 带阴影的矩形
                        Rectangle {
                            id: shadowRect
                            width: 100
                            height: 60
                            color: "white"
                            radius: 10
                            layer.enabled: true
                            layer.effect: MultiEffect {
                                shadowEnabled: true
                                shadowColor: "#80000000"
                                shadowBlur: 0.5
                                shadowHorizontalOffset: 4
                                shadowVerticalOffset: 4
                            }

                            Text {
                                anchors.centerIn: parent
                                text: "阴影效果"
                            }
                        }

                        // 带内发光效果的圆形
                        Rectangle {
                            id: glowRect
                            width: 60
                            height: 60
                            radius: 30
                            color: "orange"
                            layer.enabled: true
                            layer.effect: MultiEffect {
                                shadowEnabled: true
                                shadowColor: "orange"
                                shadowBlur: 1.0
                                shadowScale: 1.5
                            }
                        }

                        // 卡片效果
                        Rectangle {
                            width: 100
                            height: 70
                            color: "white"
                            radius: 8
                            layer.enabled: true
                            layer.effect: MultiEffect {
                                shadowEnabled: true
                                shadowColor: "#40000000"
                                shadowBlur: 0.3
                                shadowHorizontalOffset: 0
                                shadowVerticalOffset: 2
                            }

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

            // 6. 模糊效果
            GroupBox {
                title: "6. Blur (模糊效果)"
                Layout.fillWidth: true

                Column {
                    spacing: 10
                    width: parent.width

                    Slider {
                        id: blurSlider
                        width: parent.width
                        from: 0
                        to: 64
                        value: 0
                    }

                    Rectangle {
                        width: parent.width
                        height: 80
                        color: "lightyellow"
                        clip: true

                        Row {
                            anchors.centerIn: parent
                            spacing: 20

                            Text {
                                text: "模糊测试"
                                font.pixelSize: 24
                                font.bold: true
                                color: "darkred"
                                layer.enabled: blurSlider.value > 0
                                layer.effect: MultiEffect {
                                    blurEnabled: true
                                    blur: blurSlider.value / 64
                                }
                            }

                            Rectangle {
                                width: 60
                                height: 60
                                color: "green"
                                radius: 10
                                layer.enabled: blurSlider.value > 0
                                layer.effect: MultiEffect {
                                    blurEnabled: true
                                    blur: blurSlider.value / 64
                                }
                            }

                            Rectangle {
                                width: 60
                                height: 60
                                gradient: Gradient {
                                    GradientStop { position: 0; color: "purple" }
                                    GradientStop { position: 1; color: "blue" }
                                }
                                layer.enabled: blurSlider.value > 0
                                layer.effect: MultiEffect {
                                    blurEnabled: true
                                    blur: blurSlider.value / 64
                                }
                            }
                        }
                    }

                    Label {
                        text: "模糊强度: " + blurSlider.value.toFixed(0)
                        font.pixelSize: 12
                        color: "gray"
                    }
                }
            }

            // 7. 颜色调整
            GroupBox {
                title: "7. 颜色调整 (Brightness/Contrast)"
                Layout.fillWidth: true

                Column {
                    spacing: 10
                    width: parent.width

                    Row {
                        spacing: 10

                        Column {
                            Label { text: "亮度" }
                            Slider {
                                id: brightnessSlider
                                width: 150
                                from: -1
                                to: 1
                                value: 0
                            }
                        }

                        Column {
                            Label { text: "对比度" }
                            Slider {
                                id: contrastSlider
                                width: 150
                                from: 0
                                to: 2
                                value: 1
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

                            // 调整后的
                            Rectangle {
                                width: 60
                                height: 60
                                color: "teal"
                                radius: 5
                                layer.enabled: true
                                layer.effect: MultiEffect {
                                    brightness: brightnessSlider.value
                                    contrast: contrastSlider.value
                                }

                                Text {
                                    anchors.centerIn: parent
                                    text: "调整后"
                                    color: "white"
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
