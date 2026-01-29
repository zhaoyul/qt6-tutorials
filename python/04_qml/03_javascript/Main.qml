import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window
import "MathUtils.js" as MathUtils

Window {
    id: root
    width: 480
    height: 600
    visible: true
    title: qsTr("QML JavaScript Integration Demo")

    // Inline JavaScript function in QML
    function formatNumber(num) {
        if (num === null) return "N/A";
        return num.toLocaleString();
    }

    ScrollView {
        anchors.fill: parent
        contentWidth: parent.width

        ColumnLayout {
            width: parent.width
            spacing: 16
            anchors.margins: 20

            // Header
            Label {
                Layout.alignment: Qt.AlignHCenter
                text: qsTr("JavaScript Integration Examples")
                font.pixelSize: 24
                font.bold: true
            }

            // Separator
            Rectangle {
                Layout.fillWidth: true
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                height: 1
                color: "#cccccc"
            }

            // Factorial Section
            GroupBox {
                Layout.fillWidth: true
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                title: qsTr("Factorial (MathUtils.factorial)")

                ColumnLayout {
                    width: parent.width

                    SpinBox {
                        id: factorialInput
                        from: 0
                        to: 20
                        value: 5
                        editable: true
                    }

                    Button {
                        text: qsTr("Calculate Factorial")
                        onClicked: {
                            // Call JavaScript function from MathUtils.js
                            let result = MathUtils.factorial(factorialInput.value);
                            factorialResult.text = formatNumber(result);
                        }
                    }

                    Label {
                        id: factorialResult
                        text: qsTr("Result will appear here")
                        font.pixelSize: 14
                        color: "#2196F3"
                    }
                }
            }

            // Fibonacci Section
            GroupBox {
                Layout.fillWidth: true
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                title: qsTr("Fibonacci (MathUtils.fibonacci)")

                ColumnLayout {
                    width: parent.width

                    SpinBox {
                        id: fibonacciInput
                        from: 0
                        to: 40
                        value: 10
                        editable: true
                    }

                    Button {
                        text: qsTr("Calculate Fibonacci")
                        onClicked: {
                            // Call JavaScript function from MathUtils.js
                            let result = MathUtils.fibonacci(fibonacciInput.value);
                            fibonacciResult.text = formatNumber(result);
                        }
                    }

                    Label {
                        id: fibonacciResult
                        text: qsTr("Result will appear here")
                        font.pixelSize: 14
                        color: "#2196F3"
                    }
                }
            }

            // Prime Check Section
            GroupBox {
                Layout.fillWidth: true
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                title: qsTr("Prime Check (MathUtils.isPrime)")

                ColumnLayout {
                    width: parent.width

                    SpinBox {
                        id: primeInput
                        from: 1
                        to: 9999
                        value: 17
                        editable: true
                    }

                    Button {
                        text: qsTr("Check Prime")
                        onClicked: {
                            // Call JavaScript function from MathUtils.js
                            let isPrime = MathUtils.isPrime(primeInput.value);
                            primeResult.text = isPrime ? qsTr("✓ Yes, prime!") : qsTr("✗ Not prime");
                            primeResult.color = isPrime ? "#4CAF50" : "#F44336";
                        }
                    }

                    Label {
                        id: primeResult
                        text: qsTr("Result will appear here")
                        font.pixelSize: 14
                        color: "#2196F3"
                    }
                }
            }

            // Sum and Average Section
            GroupBox {
                Layout.fillWidth: true
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                title: qsTr("Sum & Average (MathUtils.sum, MathUtils.average)")

                ColumnLayout {
                    width: parent.width

                    Label {
                        text: qsTr("Enter numbers (comma-separated):")
                    }

                    TextField {
                        id: numbersInput
                        Layout.fillWidth: true
                        text: "10, 20, 30, 40, 50"
                        placeholderText: qsTr("e.g., 1, 2, 3, 4, 5")
                    }

                    RowLayout {
                        Button {
                            text: qsTr("Calculate Sum")
                            onClicked: {
                                // Parse the input string into an array
                                let numbers = numbersInput.text.split(',').map(s => parseFloat(s.trim()));
                                // Call JavaScript function from MathUtils.js
                                let result = MathUtils.sum(numbers);
                                sumAvgResult.text = qsTr("Sum: %1").arg(result.toLocaleString());
                            }
                        }

                        Button {
                            text: qsTr("Calculate Average")
                            onClicked: {
                                // Parse the input string into an array
                                let numbers = numbersInput.text.split(',').map(s => parseFloat(s.trim()));
                                // Call JavaScript function from MathUtils.js
                                let result = MathUtils.average(numbers);
                                sumAvgResult.text = qsTr("Average: %1").arg(result.toLocaleString(undefined, 'f', 2));
                            }
                        }
                    }

                    Label {
                        id: sumAvgResult
                        text: qsTr("Result will appear here")
                        font.pixelSize: 14
                        color: "#2196F3"
                    }
                }
            }

            // Random Number Section
            GroupBox {
                Layout.fillWidth: true
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                title: qsTr("Random Number (MathUtils.randomInt)")

                ColumnLayout {
                    width: parent.width

                    RowLayout {
                        Label {
                            text: qsTr("Min:")
                        }
                        SpinBox {
                            id: randomMin
                            from: 0
                            to: 99
                            value: 1
                            editable: true
                        }
                        Label {
                            text: qsTr("Max:")
                        }
                        SpinBox {
                            id: randomMax
                            from: 1
                            to: 1000
                            value: 100
                            editable: true
                        }
                    }

                    Button {
                        text: qsTr("Generate Random Number")
                        onClicked: {
                            // Call JavaScript function from MathUtils.js
                            let result = MathUtils.randomInt(randomMin.value, randomMax.value);
                            randomResult.text = result.toString();
                        }
                    }

                    Label {
                        id: randomResult
                        text: qsTr("Result will appear here")
                        font.pixelSize: 14
                        color: "#2196F3"
                    }
                }
            }

            // Power Section
            GroupBox {
                Layout.fillWidth: true
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                title: qsTr("Power (MathUtils.power)")

                ColumnLayout {
                    width: parent.width

                    RowLayout {
                        Label {
                            text: qsTr("Base:")
                        }
                        SpinBox {
                            id: baseInput
                            from: 0
                            to: 100
                            value: 2
                            editable: true
                        }
                        Label {
                            text: qsTr("Exponent:")
                        }
                        SpinBox {
                            id: exponentInput
                            from: 0
                            to: 10
                            value: 8
                            editable: true
                        }
                    }

                    Button {
                        text: qsTr("Calculate Power")
                        onClicked: {
                            // Call JavaScript function from MathUtils.js
                            let result = MathUtils.power(baseInput.value, exponentInput.value);
                            powerResult.text = formatNumber(result);
                        }
                    }

                    Label {
                        id: powerResult
                        text: qsTr("Result will appear here")
                        font.pixelSize: 14
                        color: "#2196F3"
                    }
                }
            }

            // Inline JavaScript logic demo
            GroupBox {
                Layout.fillWidth: true
                Layout.leftMargin: 20
                Layout.rightMargin: 20
                title: qsTr("Inline JavaScript Demo")

                ColumnLayout {
                    width: parent.width

                    Label {
                        text: qsTr("Current time updated every second using inline JS")
                    }

                    Label {
                        id: timeLabel
                        font.pixelSize: 18
                        font.bold: true
                        color: "#FF9800"
                    }

                    Timer {
                        interval: 1000
                        running: true
                        repeat: true
                        onTriggered: {
                            // Inline JavaScript logic directly in QML
                            let now = new Date();
                            timeLabel.text = now.toLocaleTimeString();
                        }
                    }
                }
            }

            // Spacer
            Item {
                Layout.fillHeight: true
                Layout.minimumHeight: 20
            }
        }
    }
}
