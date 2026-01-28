# Qt 3D module (optional)
# Requires Qt 3D components.

find_package(Qt6 COMPONENTS 3DCore 3DRender 3DExtras QUIET)

if (TARGET Qt6::3DCore AND TARGET Qt6::3DRender AND TARGET Qt6::3DExtras)
  add_subdirectory(01_basics)
else()
  message(STATUS "Qt 3D modules not found, skipping optional demos.")
endif()
