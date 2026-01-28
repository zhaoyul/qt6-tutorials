# Qt Multimedia module (optional)
# Requires system multimedia backend support.

find_package(Qt6 COMPONENTS Multimedia QUIET)

if (Qt6Multimedia_FOUND)
  add_subdirectory(01_audio)
  add_subdirectory(02_video)
  add_subdirectory(03_camera)
else()
  message(STATUS "Qt Multimedia module not found, skipping optional demos.")
endif()
