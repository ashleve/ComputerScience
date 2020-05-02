cmake_minimum_required(VERSION 3.16)
project(scr2 C)

set(CMAKE_C_STANDARD 11)

add_executable(scr2 main.c)
TARGET_LINK_LIBRARIES(scr2 rt)
TARGET_LINK_LIBRARIES(scr2 pthread)