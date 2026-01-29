import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    width: 520
    height: 480
    visible: true
    title: "QML Types Demo"

    property int count: 3
    property real ratio: 0.75
    property string labelText: "Type Examples"
    property color accent: "#4a90e2"
    property var items: ["Alpha", "Beta", "Gamma"]

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 10

        Label {
            text: labelText
            font.pixelSize: 22
            color: accent
        }

        Label { text: "int: " + count }
        Label { text: "real: " + ratio }
        Label { text: "string: " + labelText }
        Label { text: "color: " + accent }

        RowLayout {
            spacing: 8
            Label { text: "list:" }
            Repeater {
                model: items
                delegate: Label { text: (index + 1) + ". " + modelData }
            }
        }

        Button {
            text: "Increment"
            onClicked: count += 1
        }
    }
}
