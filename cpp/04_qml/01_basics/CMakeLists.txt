qt_add_executable(qml_basics_demo main.cpp)

qt_add_qml_module(qml_basics_demo
    URI QmlBasics
    VERSION 1.0
    QML_FILES
        Main.qml
)

target_link_libraries(qml_basics_demo PRIVATE Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick)
