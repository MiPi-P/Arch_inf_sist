cmake_minimum_required(VERSION 3.10)

project(robot)

set(CMAKE_CXX_STANDARD 14)

add_executable(robot
        main.cpp
        app.cpp
        foo_receiver.cpp
        foo_engine.cpp
)