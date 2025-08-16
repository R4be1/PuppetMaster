#ifndef SSLSHELL_SHELL_H
#define SSLSHELL_SHELL_H

#include <openssl/ssl.h>
#include <openssl/err.h>

void SSL_shell(SSL *ssl);

#endif // SSLSHELL_SHELL_H