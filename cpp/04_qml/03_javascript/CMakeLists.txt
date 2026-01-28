qt_add_executable(qml_javascript_demo main.cpp)

qt_add_qml_module(qml_javascript_demo
    URI QmlJavaScript
    VERSION 1.0
    QML_FILES
        Main.qml
        MathUtils.js
)

target_link_libraries(qml_javascript_demo PRIVATE Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick)
