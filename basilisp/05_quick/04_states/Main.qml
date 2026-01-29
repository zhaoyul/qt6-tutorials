/**
 * Qt Quick States & Transitions 示例
 *
 * 展示内容：
 * - State: 状态定义
 * - PropertyChanges: 属性变化
 * - Transition: 过渡动画
 * - AnchorChanges: 锚点变化
 */

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 600
    height: 700
    visible: true
    title: "Qt Quick States & Transitions"

    ScrollView {
        anchors.fill: parent

        ColumnLayout {
            width: root.width - 40
            x: 20
            spacing: 15

            Label {
                text: "States & Transitions 状态机"
                font.pixelSize: 24
                font.bold: true
                Layout.topMargin: 20
            }

            // 1. 基础状态切换
            GroupBox {
                title: "1. 基础状态切换"
                Layout.fillWidth: true

                Column {
                    spacing: 10
                    width: parent.width

                    Rectangle {
                        id: stateRect
                        width: 120
                        height: 60
                        color: "steelblue"
                        radius: 10

                        Text {
                            anchors.centerIn: parent
                            text: stateRect.state === "" ? "正常" : (stateRect.state === "expanded" ? "展开" : "隐藏")
                            color: "white"
                            font.bold: true
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                if (stateRect.state === "")
                                    stateRect.state = "expanded"
                                else if (stateRect.state === "expanded")
                                    stateRect.state = "hidden"
                                else
                                    stateRect.state = ""
                            }
                        }

                        states: [
                            State {
                                name: "expanded"
                                PropertyChanges {
                                    target: stateRect
                                    width: 200
                                    height: 100
                                    color: "seagreen"
                                }
                            },
                            State {
                                name: "hidden"
                                PropertyChanges {
                                    target: stateRect
                                    width: 60
                                    height: 40
                                    color: "crimson"
                                    opacity: 0.6
                                }
                            }
                        ]

                        transitions: [
                            Transition {
                                from: "*"; to: "*"
                                ParallelAnimation {
                                    NumberAnimation {
                                        properties: "width,height"
                                        duration: 300
                                        easing.type: Easing.InOutQuad
                                    }
                                    ColorAnimation {
                                        duration: 300
                                    }
                                    NumberAnimation {
                                        property: "opacity"
                                        duration: 300
                                    }
                                }
                            }
                        ]
                    }

                    Label {
                        text: "点击矩形切换状态: 正常 → 展开 → 隐藏"
                        font.pixelSize: 12
                        color: "gray"
                    }
                }
            }

            // 2. 位置状态切换
            GroupBox {
                title: "2. 位置状态切换 (AnchorChanges)"
                Layout.fillWidth: true

                Rectangle {
                    width: parent.width
                    height: 100
                    color: "#f5f5f5"
                    border.color: "#ddd"

                    Rectangle {
                        id: movingBox
                        width: 80
                        height: 60
                        color: "orange"
                        radius: 8
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 10

                        Text {
                            anchors.centerIn: parent
                            text: "点击移动"
                            color: "white"
                            font.bold: true
                        }

                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                movingBox.state = movingBox.state === "right" ? "" : "right"
                            }
                        }

                        states: [
                            State {
                                name: "right"
                                AnchorChanges {
                                    target: movingBox
                                    anchors.left: undefined
                                    anchors.right: parent.right
                                }
                                PropertyChanges {
                                    target: movingBox
                                    anchors.rightMargin: 10
                                    color: "purple"
                                }
                            }
                        ]

                        transitions: [
                            Transition {
                                AnchorAnimation {
                                    duration: 400
                                    easing.type: Easing.OutBounce
                                }
                                ColorAnimation {
                                    duration: 400
                                }
                            }
                        ]
                    }
                }
            }

            // 3. 多元素联动状态
            GroupBox {
                title: "3. 多元素联动状态"
                Layout.fillWidth: true

                Column {
                    spacing: 15
                    width: parent.width

                    Row {
                        spacing: 10

                        Button {
                            text: "登录状态"
                            onClicked: loginContainer.state = "loggedIn"
                        }

                        Button {
                            text: "登出状态"
                            onClicked: loginContainer.state = ""
                        }

                        Button {
                            text: "加载状态"
                            onClicked: loginContainer.state = "loading"
                        }
                    }

                    Rectangle {
                        id: loginContainer
                        width: parent.width
                        height: 120
                        color: "#f0f0f0"
                        radius: 8

                        Row {
                            anchors.centerIn: parent
                            spacing: 20

                            Rectangle {
                                id: userIcon
                                width: 60
                                height: 60
                                radius: 30
                                color: "lightgray"

                                Text {
                                    anchors.centerIn: parent
                                    text: "?"
                                    font.pixelSize: 24
                                    color: "white"
                                }
                            }

                            Column {
                                anchors.verticalCenter: parent.verticalCenter
                                spacing: 5

                                Text {
                                    id: statusText
                                    text: "未登录"
                                    font.bold: true
                                }

                                Text {
                                    id: detailText
                                    text: "请点击登录按钮"
                                    font.pixelSize: 12
                                    color: "gray"
                                }
                            }

                            BusyIndicator {
                                id: loadingIndicator
                                running: false
                                visible: false
                            }
                        }

                        states: [
                            State {
                                name: "loggedIn"
                                PropertyChanges {
                                    target: userIcon
                                    color: "seagreen"
                                }
                                PropertyChanges {
                                    target: statusText
                                    text: "已登录"
                                }
                                PropertyChanges {
                                    target: detailText
                                    text: "欢迎回来!"
                                }
                            },
                            State {
                                name: "loading"
                                PropertyChanges {
                                    target: statusText
                                    text: "登录中..."
                                }
                                PropertyChanges {
                                    target: detailText
                                    text: "请稍候"
                                }
                                PropertyChanges {
                                    target: loadingIndicator
                                    running: true
                                    visible: true
                                }
                            }
                        ]

                        transitions: [
                            Transition {
                                from: "*"; to: "*"
                                ColorAnimation {
                                    duration: 300
                                }
                            }
                        ]
                    }
                }
            }

            // 4. 条件状态 (when 属性)
            GroupBox {
                title: "4. 条件状态 (when)"
                Layout.fillWidth: true

                Column {
                    spacing: 10
                    width: parent.width

                    Switch {
                        id: toggleSwitch
                        text: "启用高级模式"
                    }

                    Rectangle {
                        id: conditionalRect
                        width: parent.width
                        height: toggleSwitch.checked ? 150 : 80
                        color: toggleSwitch.checked ? "darkblue" : "lightblue"
                        radius: 10

                        // 使用 when 自动切换状态
                        state: toggleSwitch.checked ? "advanced" : ""

                        states: [
                            State {
                                name: "advanced"
                                PropertyChanges {
                                    target: conditionalRect
                                    height: 150
                                    color: "darkblue"
                                }
                                PropertyChanges {
                                    target: advancedContent
                                    opacity: 1
                                    visible: true
                                }
                            }
                        ]

                        transitions: [
                            Transition {
                                NumberAnimation {
                                    properties: "height,opacity"
                                    duration: 300
                                    easing.type: Easing.InOutQuad
                                }
                                ColorAnimation {
                                    duration: 300
                                }
                            }
                        ]

                        Column {
                            anchors.centerIn: parent
                            spacing: 10

                            Text {
                                text: toggleSwitch.checked ? "高级模式已启用" : "基础模式"
                                color: toggleSwitch.checked ? "white" : "black"
                                font.bold: true
                                anchors.horizontalCenter: parent.horizontalCenter
                            }

                            Column {
                                id: advancedContent
                                opacity: 0
                                visible: false
                                spacing: 5

                                Text {
                                    text: "• 高级功能 A"
                                    color: "white"
                                    font.pixelSize: 12
                                }
                                Text {
                                    text: "• 高级功能 B"
                                    color: "white"
                                    font.pixelSize: 12
                                }
                                Text {
                                    text: "• 高级功能 C"
                                    color: "white"
                                    font.pixelSize: 12
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
