#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#include "utils.h"

/*
    split_command() will tokenize a string into an array using " " as the delimiter unless quotes are present
    in this case it will be very useful for working with custom commands

    usage example:
    char *test_input = "cd \"Downloads/new test/main\" && mousepad 'new build/main.txt' -option";
    char **words = NULL;
    int wordCount = 0;
    split_command(test_input, &words, &wordCount);

    resulting array would look like this:
    ["cd", ""Downloads/new test/main"", "&&", "mousepad", "'new build/main.txt'", "-option"]
*/

void cleanup_argarray(char ***words, int *wordCount)
{
    for (int i = 0; i < *wordCount; i++)
    {
        free((*words)[i]);
    }
    free(*words);
    *words = NULL;
    *wordCount = 0;
}

// function to reduce duplicated code
void process_word(char ***words, int *wordCount, char *word, int wordIndex)
{
    // Trim trailing spaces from the word
    while (wordIndex > 0 && isspace((unsigned char)word[wordIndex - 1]))
    {
        wordIndex--;
    }
    // add word to array
    word[wordIndex] = '\0';
    *words = realloc(*words, sizeof(char *) * (*wordCount + 1));
    if (*words == NULL)
    {
        fprintf(stderr, "Error: memory allocation failed\n");
        cleanup_argarray(words, wordCount);
        exit(1);
    }
    (*words)[*wordCount] = word;
    (*wordCount)++;
}

int split_command(char *input, char ***words, int *wordCount)
{
    *words = NULL;
    char *word = NULL;
    int wordIndex = 0;
    int inQuote = 0;
    int inputLen = strlen(input);

    if (inputLen < 1)
    {
        fprintf(stderr, "Error: input had 0 length\n");
        cleanup_argarray(words, wordCount);
        return 1;
    }

    for (int i = 0; i < inputLen; i++)
    {
        char c = input[i];
        if (c == '\'' || c == '\"')
        {
            if (!inQuote && word != NULL)
            {
                process_word(words, wordCount, word, wordIndex);
                word = NULL;
            }
            inQuote = !inQuote;
        }
        else if (c == ' ' && !inQuote)
        {
            if (word != NULL)
            {
                process_word(words, wordCount, word, wordIndex);
                word = NULL;
            }
        }
        else
        {
            if (word == NULL)
            {
                word = malloc(sizeof(char) * (inputLen + 1)); // Increased size by 1 to accommodate null character
                if (word == NULL)
                {
                    fprintf(stderr, "Error: memory allocation failed\n");
                    cleanup_argarray(words, wordCount);
                    return 1;
                }
                wordIndex = 0;
            }
            word[wordIndex++] = c;
        }
    }

    if (word != NULL)
    {
        process_word(words, wordCount, word, wordIndex);
    }

    *words = realloc(*words, sizeof(char *) * (*wordCount + 1));
    if (*words == NULL)
    {
        fprintf(stderr, "Error: memory allocation failed\n");
        cleanup_argarray(words, wordCount);
        return 1;
    }
    (*words)[*wordCount] = NULL;
    return 0;
}
