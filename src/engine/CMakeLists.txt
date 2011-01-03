# src/engine/
project (HEDGEHOGHD_ENGINE)

# This component really only uses QtCore.  Can I specify that here?
find_package (Qt4 4.4.1 REQUIRED)

INCLUDE(FindPkgConfig)
pkg_check_modules(QJSON QJson=>0.7.1)

if (NOT QJSON_FOUND)
  message(FATAL_ERROR "Need QJson in order to build!")
endif (NOT QJSON_FOUND)

include (${QT_USE_FILE})

set (HHD_ENGINE_CXX_SRCS
  chunk.cpp
  game.cpp
  zone.cpp
  act.cpp
  layout.cpp
)

set (ENGINE_MOCS
  )

qt4_wrap_cpp (HHD_ENGINE_CXX_SRCS ${HHD_ENGINE_MOCS})


add_library (hedgehoghd_engine SHARED ${HHD_ENGINE_CXX_SRCS})
