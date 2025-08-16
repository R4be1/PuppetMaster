CFLAGS = -Wall -Wextra -std=gnu99
LDFLAGS = -lssl -lcrypto

SRC = main.c shell.c utils.c

.PHONY: all

all:
	@echo "Please specify the target platform: 'make windows' or 'make linux'"

# to get openssl to work with windows cross-compilation create a new directory and run these commands
# 1. git clone https://github.com/openssl/openssl.git && cd openssl
# 2. ./Configure --cross-compile-prefix=x86_64-w64-mingw32- mingw64
# 3. make
# 
# then replace the absolute path of the openssl directory into CFLAGS and LDFLAGS as shown below
windows: CC = x86_64-w64-mingw32-gcc
windows: CFLAGS += -I/path/to/openssl/include -DUNICODE -D_UNICODE -DWIN32_LEAN_AND_MEAN
windows: LDFLAGS += -L/path/to/openssl/ -lws2_32
windows: sslshell

linux: CC = gcc
linux: sslshell

sslshell: $(SRC)
	$(CC) $(SRC) -o sslshell $(CFLAGS) $(LDFLAGS)

.PHONY: clean
clean:
	rm -f sslshell*
