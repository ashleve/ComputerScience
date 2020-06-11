cmake_minimum_required(VERSION 3.16)
project(Zadanie_3_Server C)

set(CMAKE_C_STANDARD 11)

add_executable(Zadanie_3_Server main.c task.h task.c list.c list.h msg.h msg.c)

TARGET_LINK_LIBRARIES(Zadanie_3_Server rt)
TARGET_LINK_LIBRARIES(Zadanie_3_Server pthread)