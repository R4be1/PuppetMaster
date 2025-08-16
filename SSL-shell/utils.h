#ifndef SSLSHELL_UTILS_H
#define SSLSHELL_UTILS_H

int split_command(char *input, char ***words, int *wordCount);
void cleanup_argarray(char ***words, int *wordCount);

#endif // SSLSHELL_UTILS_H