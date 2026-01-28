qt_add_executable(qml_types_demo main.cpp)

qt_add_qml_module(qml_types_demo
    URI QmlTypes
    VERSION 1.0
    QML_FILES
        Main.qml
)

target_link_libraries(qml_types_demo PRIVATE Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick)
