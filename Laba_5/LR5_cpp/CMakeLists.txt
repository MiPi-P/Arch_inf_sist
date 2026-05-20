cmake_minimum_required(VERSION 3.15)
project(RobotLab5 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)

include(FetchContent)

FetchContent_Declare(
        httplib
        GIT_REPOSITORY https://github.com/yhirose/cpp-httplib.git
        GIT_SHALLOW TRUE
)

set(HTTPLIB_USE_NON_BLOCKING_GETADDRINFO OFF CACHE BOOL "" FORCE)

FetchContent_MakeAvailable(httplib)

FetchContent_Declare(
        json
        GIT_REPOSITORY https://github.com/nlohmann/json.git
)
FetchContent_MakeAvailable(json)

add_executable(robot_lab5
        main.cpp
        foo_engine.cpp
)

target_link_libraries(robot_lab5 PRIVATE httplib)
target_link_libraries(robot_lab5 PRIVATE nlohmann_json::nlohmann_json)

target_compile_definitions(robot_lab5 PRIVATE _WIN32_WINNT=0x0A00 WINVER=0x0A00)
