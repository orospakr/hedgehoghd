# src/editor/
project (HEDGEHOGHD_EDITOR)
find_package (Qt4 4.4.1 REQUIRED)

INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR} ${HEDGEHOGHD_EDITOR_SOURCE_DIR} ${HEDGEHOGHD_EDITOR_BINARY_DIR})

include (${QT_USE_FILE})


set (HHD_EDITOR_CXX_SRCS
  hedgehoghd_editor_main.cpp
  testdialog.cpp
)

set (HHD_EDITOR_UIS
  testdialog.ui
)

qt4_wrap_ui (HHD_EDITOR_CXX_SRCS ${HHD_EDITOR_UIS})

qt4_wrap_cpp (HHD_EDITOR_CXX_SRCS testdialog.h)
  

add_executable (hedgehoghd_editor ${HHD_EDITOR_CXX_SRCS})

target_link_libraries (hedgehoghd_editor ${QT_LIBRARIES})
