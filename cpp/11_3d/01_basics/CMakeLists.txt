add_executable(qt3d_basics_demo main.cpp)

target_link_libraries(qt3d_basics_demo PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::3DCore
    Qt6::3DRender
    Qt6::3DExtras
)
