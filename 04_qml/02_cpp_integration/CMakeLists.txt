qt_add_executable(qml_cpp_demo main.cpp counter.cpp counter.h)

qt_add_qml_module(qml_cpp_demo
    URI QmlCppIntegration
    VERSION 1.0
    QML_FILES
        Main.qml
)

target_link_libraries(qml_cpp_demo PRIVATE Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick)
