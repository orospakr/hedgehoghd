# src/editor/
project (HEDGEHOGHD_EDITOR)
find_package (Qt4 4.4.1 REQUIRED)

INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR} ${HEDGEHOGHD_EDITOR_SOURCE_DIR} ${HEDGEHOGHD_EDITOR_BINARY_DIR} ${HEDGEHOGHD_ENGINE_SOURCE_DIR} ${HEDGEHOG_ENGINE_BINARY_DIR})

# dang, how does this change the results of ${QT_USE_FILE}?  I guess QT_USE_FILE
# is actually a full macro.
SET(QT_USE_QTSVG TRUE)

include (${QT_USE_FILE})


set (HHD_EDITOR_CXX_SRCS
  hedgehoghd_editor_main.cpp
  testdialog.cpp
  editor_application.cpp
  editor_window.cpp
)

set (HHD_EDITOR_UIS
  testdialog.ui
)

set (HHD_EDITOR_MOCS
  testdialog.h
  editor_application.h
  editor_window.h
)

qt4_wrap_ui (HHD_EDITOR_CXX_SRCS ${HHD_EDITOR_UIS})
qt4_wrap_cpp (HHD_EDITOR_CXX_SRCS ${HHD_EDITOR_MOCS})
  
add_executable (hedgehoghd_editor ${HHD_EDITOR_CXX_SRCS})
target_link_libraries (hedgehoghd_editor ${QT_LIBRARIES})
