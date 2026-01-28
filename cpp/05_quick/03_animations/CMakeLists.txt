qt_add_executable(quick_animations_demo main.cpp)

qt_add_qml_module(quick_animations_demo
    URI QuickAnimations
    VERSION 1.0
    QML_FILES
        Main.qml
)

target_link_libraries(quick_animations_demo PRIVATE Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick)
