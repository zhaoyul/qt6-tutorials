/**
 * Qt Quick 动画系统示例
 *
 * 动画类型：
 * - PropertyAnimation: 属性动画
 * - NumberAnimation: 数值动画
 * - ColorAnimation: 颜色动画
 * - RotationAnimation: 旋转动画
 * - SequentialAnimation: 顺序动画
 * - ParallelAnimation: 并行动画
 * - Behavior: 行为动画
 */

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 600
    height: 700
    visible: true
    title: "Qt Quick Animations"

    ScrollView {
        anchors.fill: parent

        ColumnLayout {
            width: root.width - 40
            x: 20
            spacing: 15

            Label {
                text: "Qt Quick 动画示例"
                font.pixelSize: 24
                font.bold: true
                Layout.topMargin: 20
            }

            // 1. 基础属性动画
            GroupBox {
                title: "1. PropertyAnimation"
                Layout.fillWidth: true

                Column {
                    spacing: 10

                    Rectangle {
                        id: rect1
                        width: 60; height: 60
                        color: "coral"
                        radius: 10

                        PropertyAnimation on x {
                            from: 0
                            to: 300
                            duration: 2000
                            loops: Animation.Infinite
                            easing.type: Easing.InOutQuad
                        }
                    }

                    Label { text: "自动循环动画 (Easing.InOutQuad)" }
                }
            }

            // 2. 点击触发动画
            GroupBox {
                title: "2. 点击触发动画"
                Layout.fillWidth: true

                Column {
                    spacing: 10

                    Rectangle {
                        id: rect2
                        width: 60; height: 60
                        color: "steelblue"
                        radius: 30

                        MouseArea {
                            anchors.fill: parent
                            onClicked: clickAnim.start()
                        }

                        SequentialAnimation {
                            id: clickAnim

                            // 缩放
                            NumberAnimation {
                                target: rect2
                                property: "scale"
                                to: 1.5
                                duration: 200
                            }

                            NumberAnimation {
                                target: rect2
                                property: "scale"
                                to: 1.0
                                duration: 200
                            }
                        }
                    }

                    Label { text: "点击圆形触发缩放动画" }
                }
            }

            // 3. 并行动画
            GroupBox {
                title: "3. ParallelAnimation"
                Layout.fillWidth: true

                Column {
                    spacing: 10

                    Rectangle {
                        id: rect3
                        width: 60; height: 60
                        color: "purple"
                        opacity: 1.0

                        MouseArea {
                            anchors.fill: parent
                            onClicked: parallelAnim.start()
                        }

                        ParallelAnimation {
                            id: parallelAnim

                            NumberAnimation {
                                target: rect3
                                property: "x"
                                to: rect3.x === 0 ? 200 : 0
                                duration: 500
                            }

                            NumberAnimation {
                                target: rect3
                                property: "rotation"
                                to: rect3.rotation + 180
                                duration: 500
                            }

                            ColorAnimation {
                                target: rect3
                                property: "color"
                                to: rect3.color === "#800080" ? "orange" : "purple"
                                duration: 500
                            }
                        }
                    }

                    Label { text: "点击：同时移动 + 旋转 + 变色" }
                }
            }

            // 4. Behavior 自动动画
            GroupBox {
                title: "4. Behavior (自动动画)"
                Layout.fillWidth: true

                Column {
                    spacing: 10

                    Rectangle {
                        id: rect4
                        width: 60; height: 60
                        color: "green"
                        radius: 10
                        x: 0

                        // 任何 x 属性变化都会自动动画
                        Behavior on x {
                            NumberAnimation { duration: 300; easing.type: Easing.OutBounce }
                        }

                        Behavior on color {
                            ColorAnimation { duration: 300 }
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                rect4.x = Math.random() * 300
                                rect4.color = Qt.rgba(Math.random(), Math.random(), Math.random(), 1)
                            }
                        }
                    }

                    Label { text: "点击：Behavior 自动处理属性变化" }
                }
            }

            // 5. 状态和转换
            GroupBox {
                title: "5. States + Transitions"
                Layout.fillWidth: true

                Column {
                    spacing: 10

                    Rectangle {
                        id: rect5
                        width: 100; height: 60
                        radius: 10
                        color: "teal"

                        Text {
                            anchors.centerIn: parent
                            text: rect5.state === "" ? "正常" : "激活"
                            color: "white"
                            font.bold: true
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: rect5.state = rect5.state === "" ? "active" : ""
                        }

                        // 定义状态
                        states: [
                            State {
                                name: "active"
                                PropertyChanges {
                                    target: rect5
                                    width: 200
                                    color: "crimson"
                                }
                            }
                        ]

                        // 定义转换动画
                        transitions: [
                            Transition {
                                from: ""; to: "active"
                                ParallelAnimation {
                                    NumberAnimation { property: "width"; duration: 300 }
                                    ColorAnimation { duration: 300 }
                                }
                            },
                            Transition {
                                from: "active"; to: ""
                                ParallelAnimation {
                                    NumberAnimation { property: "width"; duration: 300 }
                                    ColorAnimation { duration: 300 }
                                }
                            }
                        ]
                    }

                    Label { text: "点击切换状态 (States + Transitions)" }
                }
            }

            // 6. 缓动函数展示
            GroupBox {
                title: "6. 缓动函数 (Easing)"
                Layout.fillWidth: true

                Column {
                    spacing: 5

                    Repeater {
                        model: [
                            { name: "Linear", type: Easing.Linear },
                            { name: "InOutQuad", type: Easing.InOutQuad },
                            { name: "OutBounce", type: Easing.OutBounce },
                            { name: "OutElastic", type: Easing.OutElastic }
                        ]

                        Row {
                            spacing: 10

                            Label {
                                width: 80
                                text: modelData.name
                            }

                            Rectangle {
                                id: easingRect
                                width: 30; height: 20
                                color: "dodgerblue"
                                radius: 5
                                x: 0

                                NumberAnimation on x {
                                    from: 0
                                    to: 200
                                    duration: 2000
                                    loops: Animation.Infinite
                                    easing.type: modelData.type
                                }
                            }
                        }
                    }
                }
            }

            // 7. 路径动画
            GroupBox {
                title: "7. PathAnimation"
                Layout.fillWidth: true

                Item {
                    width: parent.width
                    height: 120

                    // 绘制路径
                    Canvas {
                        anchors.fill: parent
                        onPaint: {
                            var ctx = getContext("2d")
                            ctx.strokeStyle = "#ccc"
                            ctx.lineWidth = 2
                            ctx.beginPath()
                            ctx.moveTo(20, 100)
                            ctx.quadraticCurveTo(150, 20, 280, 100)
                            ctx.stroke()
                        }
                    }

                    Rectangle {
                        id: pathRect
                        width: 20; height: 20
                        color: "red"
                        radius: 10

                        PathAnimation {
                            target: pathRect
                            running: true
                            loops: Animation.Infinite
                            duration: 2000

                            path: Path {
                                startX: 20; startY: 100
                                PathQuad { x: 280; y: 100; controlX: 150; controlY: 20 }
                            }
                        }
                    }
                }
            }

            Item { height: 20 }
        }
    }
}
