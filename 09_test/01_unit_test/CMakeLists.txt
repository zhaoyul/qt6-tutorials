add_executable(unit_test_demo main.cpp)
target_link_libraries(unit_test_demo PRIVATE Qt6::Core Qt6::Test)

# 注册测试
add_test(NAME UnitTestDemo COMMAND unit_test_demo)
