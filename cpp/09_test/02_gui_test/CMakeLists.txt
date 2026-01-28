add_executable(gui_test_demo main.cpp)
target_link_libraries(gui_test_demo PRIVATE Qt6::Core Qt6::Test Qt6::Widgets)

add_test(NAME GuiTestDemo COMMAND gui_test_demo)
