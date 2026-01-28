qt_add_executable(quick_effects_demo main.cpp)

qt_add_qml_module(quick_effects_demo
    URI QuickEffects
    VERSION 1.0
    QML_FILES
        Main.qml
)

target_link_libraries(quick_effects_demo PRIVATE Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick)
