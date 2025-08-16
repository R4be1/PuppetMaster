cmake_minimum_required(VERSION 3.20)
project(sslshell LANGUAGES C)

set(SERVER_HOST "127.0.0.1" CACHE STRING "LHOST (default: 127.0.0.1)")
set(SERVER_PORT "8080"      CACHE STRING "LPORT (default: 8080)")
message(STATUS "SERVER_HOST: ${SERVER_HOST}")
message(STATUS "SERVER_PORT: ${SERVER_PORT}")

add_executable(sslshell main.c shell.c utils.c)
set_property(TARGET sslshell PROPERTY
    MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>"
)

#set(OPENSSL_USE_STATIC_LIBS TRUE)
find_package(OpenSSL REQUIRED)

target_compile_features(sslshell PRIVATE c_std_99)
target_compile_definitions(sslshell PUBLIC
    UNICODE
    _UNICODE
    WIN32_LEAN_AND_MEAN
    SERVER_HOST="${SERVER_HOST}"
    SERVER_PORT="${SERVER_PORT}")

target_link_libraries(sslshell Ws2_32 OpenSSL::SSL OpenSSL::Crypto)
