/**
 * Qt Quick Controls 示例
 *
 * 展示内容：
 * - Button: 按钮
 * - Slider: 滑块
 * - ComboBox: 下拉框
 * - CheckBox: 复选框
 * - RadioButton: 单选按钮
 * - TextField: 文本输入
 * - Switch: 开关
 * - ProgressBar: 进度条
 */

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 500
    height: 700
    visible: true
    title: "Qt Quick Controls"

    // 表单数据
    property string userName: ""
    property int age: 25
    property string gender: "male"
    property bool newsletter: false
    property string country: ""
    property real progress: 0.5

    ScrollView {
        anchors.fill: parent

        ColumnLayout {
            width: root.width - 40
            x: 20
            spacing: 15

            Label {
                text: "用户信息表单"
                font.pixelSize: 24
                font.bold: true
                Layout.topMargin: 20
                Layout.alignment: Qt.AlignHCenter
            }

            // 1. TextField - 姓名输入
            GroupBox {
                title: "姓名"
                Layout.fillWidth: true

                Column {
                    spacing: 5
                    width: parent.width

                    TextField {
                        id: nameField
                        width: parent.width
                        placeholderText: "请输入姓名"
                        text: root.userName
                        onTextChanged: root.userName = text
                    }

                    Label {
                        text: "当前输入: " + (root.userName || "(空)")
                        font.pixelSize: 12
                        color: "gray"
                    }
                }
            }

            // 2. Slider - 年龄选择
            GroupBox {
                title: "年龄: " + root.age
                Layout.fillWidth: true

                Slider {
                    id: ageSlider
                    width: parent.width
                    from: 18
                    to: 100
                    value: root.age
                    stepSize: 1
                    snapMode: Slider.SnapAlways
                    onValueChanged: root.age = value
                }
            }

            // 3. RadioButton - 性别选择
            GroupBox {
                title: "性别"
                Layout.fillWidth: true

                Row {
                    spacing: 30

                    RadioButton {
                        text: "男"
                        checked: root.gender === "male"
                        onClicked: root.gender = "male"
                    }

                    RadioButton {
                        text: "女"
                        checked: root.gender === "female"
                        onClicked: root.gender = "female"
                    }

                    RadioButton {
                        text: "其他"
                        checked: root.gender === "other"
                        onClicked: root.gender = "other"
                    }
                }
            }

            // 4. ComboBox - 国家选择
            GroupBox {
                title: "国家/地区"
                Layout.fillWidth: true

                ComboBox {
                    id: countryCombo
                    width: parent.width
                    model: ["请选择", "中国", "美国", "日本", "德国", "英国", "法国", "其他"]
                    currentIndex: 0
                    onCurrentTextChanged: {
                        if (currentIndex > 0) {
                            root.country = currentText
                        } else {
                            root.country = ""
                        }
                    }
                }
            }

            // 5. CheckBox - 订阅选项
            GroupBox {
                title: "选项"
                Layout.fillWidth: true

                Column {
                    spacing: 10

                    CheckBox {
                        text: "订阅新闻邮件"
                        checked: root.newsletter
                        onCheckedChanged: root.newsletter = checked
                    }

                    CheckBox {
                        text: "同意服务条款"
                        checked: true
                        enabled: false
                    }
                }
            }

            // 6. Switch - 通知设置
            GroupBox {
                title: "通知设置"
                Layout.fillWidth: true

                Row {
                    spacing: 20

                    Label {
                        text: "接收推送通知:"
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Switch {
                        checked: true
                    }
                }
            }

            // 7. ProgressBar + Slider
            GroupBox {
                title: "完成度"
                Layout.fillWidth: true

                Column {
                    spacing: 10
                    width: parent.width

                    ProgressBar {
                        width: parent.width
                        value: root.progress
                    }

                    Slider {
                        width: parent.width
                        from: 0
                        to: 1
                        value: root.progress
                        onValueChanged: root.progress = value
                    }

                    Label {
                        text: Math.round(root.progress * 100) + "%"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                }
            }

            // 8. Button - 提交
            Row {
                spacing: 15
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: 10

                Button {
                    text: "重置"
                    flat: true
                    onClicked: {
                        nameField.text = ""
                        ageSlider.value = 25
                        countryCombo.currentIndex = 0
                        root.newsletter = false
                        root.progress = 0.5
                    }
                }

                Button {
                    text: "提交"
                    highlighted: true
                    onClicked: {
                        console.log("===== 提交的信息 =====")
                        console.log("姓名:", root.userName)
                        console.log("年龄:", root.age)
                        console.log("性别:", root.gender)
                        console.log("国家:", root.country)
                        console.log("订阅:", root.newsletter)
                        console.log("完成度:", Math.round(root.progress * 100) + "%")
                    }
                }
            }

            // 9. 信息显示
            GroupBox {
                title: "预览"
                Layout.fillWidth: true
                Layout.topMargin: 10

                Column {
                    spacing: 5
                    width: parent.width

                    Label { text: "姓名: " + (root.userName || "-") }
                    Label { text: "年龄: " + root.age }
                    Label { text: "性别: " + (root.gender === "male" ? "男" : root.gender === "female" ? "女" : "其他") }
                    Label { text: "国家: " + (root.country || "-") }
                    Label { text: "订阅: " + (root.newsletter ? "是" : "否") }
                }
            }

            Item { height: 20 }
        }
    }
}
