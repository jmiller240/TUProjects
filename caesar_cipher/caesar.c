#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv) {

    bool encrypt = true;
    int key = 7;
    char* filePath;
    char* message;

    for (int i = 0; i < argc; i++) {
        char arg0 = argv[i][0];

        if (arg0 == '-') {
            if (argv[i][1] == 'd') {
                encrypt = false;
            }
        }
        if ((arg0 >= 48 && arg0 <= 57) || (arg0 == '-' && (argv[i][1] >= 48 && argv[i][1] <= 57)) ) {
            int c = 0;
            int len = 0;
            while (argv[i][c] != '\0') {
                len++;
                c++;
            }

            char* tmp;
            tmp = (char*) malloc(len);

            for (int j = 0; j < len; j++) {
                tmp[j] = argv[i][j];
            }

            key = atoi(tmp);

            free(tmp);
        }
        if ((arg0 == '.' && i != 0) || arg0 == '/' || (arg0 >= 65 && arg0 <= 90) ||
                   (arg0 >= 97 && arg0 <= 122)) {
            int c = 0;
            int len = 0;
            while (argv[i][c] != '\0') {
                len++;
                c++;
            }

            filePath = (char*) malloc(len);
            for (int j = 0; j < len; j++) {
                filePath[j] = argv[i][j];
            }
        }
    }

    if (!*filePath) {
        message = (char*) malloc(100);
        fgets(message, 100, stdin);
    } else {
        FILE *fp = fopen(filePath, "rb");
        if (!fp) {
            return -1;
        } else {
            int len;
            fseek(fp, 0, SEEK_END);
            len = ftell(fp);

            message = (char *) malloc(len - 1);
            for (int i = 0; i < len; i++) {
                fseek(fp, i, SEEK_SET);
                char c;
                fread(&c, 1, 1, fp);
                message[i] = c;
            }
            fclose(fp);
        }
    }

    // if decrypting, we move the opposite direction
    if (!encrypt) {
        key = 0 - key;
    }

    //printf("Filepath = %s\n", filePath);
    //printf("Message = %s\n", message);
    //printf("Encrypt = %d\n", encrypt);
    //printf("Key = %d\n", key);

    char* cryptedMessage;
    cryptedMessage = (char*) malloc(strlen(message));

    for (int i = 0; i < strlen(message); i++) {
        //printf("message[%d] = %c\n", i, message[i]);
        if (message[i] >= 65 && message[i] <= 90) { // uppercase letters
            unsigned char letter = message[i] + key;
            if (letter > 90) {
                letter -= 26;
            } else if (letter < 65) {
                letter += 26;
            }
            cryptedMessage[i] = (char) letter;
        } else if (message[i] >= 97 && message[i] <= 122) { // lowercase letters
            unsigned char letter = message[i] + key;
            if (letter > 122) {
                letter -= 26;
            } else if (letter < 97) {
                letter += 26;
            }
            cryptedMessage[i] = (char) letter;
        } else {                                        // non-alphabetical chars
            cryptedMessage[i] = message[i];
        }
    }

    printf("%s\n", cryptedMessage);

    //for (int i = 0; i < strlen(encryptedMessage); i++) {
    //    printf("encryptedMessage[%d] = %c\n", i, encryptedMessage[i]);
    //}

    if (*filePath) {
        free(filePath);
    }
    if (*message) {
        free(message);
    }
    if (*cryptedMessage) {
        free(cryptedMessage);
    }

    return 0;
}