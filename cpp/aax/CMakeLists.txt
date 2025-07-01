cmake_minimum_required(VERSION 3.15)
project(TrueRoomAAX)

set(CMAKE_CXX_STANDARD 17)

# Expect AAX_SDK_ROOT environment variable
if(NOT DEFINED ENV{AAX_SDK_ROOT})
    message(FATAL_ERROR "AAX_SDK_ROOT environment variable not set")
endif()
set(AAX_SDK "$ENV{AAX_SDK_ROOT}")

include_directories(${AAX_SDK}/Interfaces)
include_directories(${AAX_SDK}/Utilities)

add_library(TrueRoom SHARED
    TrueRoom.cpp
    HRIR.cpp)

target_link_libraries(TrueRoom
    fftw3f
    sndfile
    ${AAX_SDK}/Libs/AAXLibrary
)
