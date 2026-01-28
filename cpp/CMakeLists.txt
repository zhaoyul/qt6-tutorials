cmake_minimum_required(VERSION 3.16)
project(qt6-demos VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# 查找 Qt6
find_package(Qt6 REQUIRED COMPONENTS
    Core
    Gui
    Widgets
    Network
    Sql
    Qml
    Quick
    Test
    Concurrent
    WebSockets
)

# 添加子目录
add_subdirectory(01_core)
add_subdirectory(02_gui)
add_subdirectory(03_widgets)
add_subdirectory(04_qml)
add_subdirectory(05_quick)
add_subdirectory(06_network)
add_subdirectory(07_sql)
add_subdirectory(08_multimedia EXCLUDE_FROM_ALL)  # 可选
add_subdirectory(09_test)
add_subdirectory(10_concurrent)
add_subdirectory(11_3d EXCLUDE_FROM_ALL)          # 可选
add_subdirectory(12_project)
