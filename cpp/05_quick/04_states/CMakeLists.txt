qt_add_executable(quick_states_demo main.cpp)

qt_add_qml_module(quick_states_demo
    URI QuickStates
    VERSION 1.0
    QML_FILES
        Main.qml
)

target_link_libraries(quick_states_demo PRIVATE Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick)
