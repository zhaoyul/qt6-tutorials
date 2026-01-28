qt_add_executable(quick_items_demo main.cpp)

qt_add_qml_module(quick_items_demo
    URI QuickItems
    VERSION 1.0
    QML_FILES
        Main.qml
)

target_link_libraries(quick_items_demo PRIVATE Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick)
