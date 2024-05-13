cmake_minimum_required(VERSION 3.14)
project(ScriptTest)

set(CMAKE_CXX_STANDARD 11)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/release-1.10.0.tar.gz
)
include(GoogleTest)
FetchContent_MakeAvailable(googletest)

add_executable(script_test script.cpp)
target_link_libraries(script_test gtest_main)

enable_testing()
include(GoogleTest)
gtest_discover_tests(script_test)
