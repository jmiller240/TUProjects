#include <unistd.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int logInfo(FILE* image) {
    int offset = 0;
    fseek(image, 10, SEEK_SET);
    fread(&offset, 4, 1, image);
    printf("Pixel array offset from start: %d\n", offset);

    int width = 0;
    fseek(image, 18, SEEK_SET);
    fread(&width, 4, 1, image);
    printf("Width of image in pixels: %d\n", width);

    int height = 0;
    fseek(image, 22, SEEK_SET);
    fread(&height, 4, 1, image);
    printf("Height of image in pixels: %d\n", height);

    return offset;
}

void encodeImage(FILE* originalImage, FILE* encodedImage, const char* message, int fileSize, int pixelArrayOffset) {
    fseek(originalImage, 0, SEEK_SET);

    // copy headers
    for(int b = 0; b < pixelArrayOffset; b++) {
        fseek(originalImage, b, SEEK_SET);
        int byte = 0;
        fread(&byte, 1, 1, originalImage);

        fwrite(&byte, 1, 1, encodedImage);
    }

    // encode message
    fseek(originalImage, pixelArrayOffset, SEEK_SET);

    int i = 0;
    int pixelByte = 0;
    unsigned int length = strlen(message);
    while (i <= length) {
        // Encode each bit of each letter of the message
        for(int c = 0; c < 8; c++) {
            // skip alpha byte
            if ((pixelByte + 1) % 4 == 0) {
                fseek(originalImage, pixelArrayOffset + pixelByte, SEEK_SET);
                int byte = 0;
                fread(&byte, 1, 1, originalImage);
                fwrite(&byte, 1, 1, encodedImage);
                pixelByte++;
                fseek(originalImage, pixelArrayOffset + pixelByte, SEEK_SET);
            } else {
                fseek(originalImage, pixelArrayOffset + pixelByte, SEEK_SET);
            }

            // change LSB
            int byte = 0;
            fread(&byte, 1, 1, originalImage);
            if ((byte % 2) != ((message[i] >> c) % 2)) {
                if (byte == 255) {
                    byte--;
                } else {
                    byte++;
                }
            }
            fwrite(&byte, 1, 1, encodedImage);

            pixelByte++;
        }

        i++;
    }

    // copy rest of image
    for(int b = pixelArrayOffset + pixelByte; b < fileSize; b++) {
        fseek(originalImage, b, SEEK_SET);
        int byte = 0;
        fread(&byte, 1, 1, originalImage);

        fwrite(&byte, 1, 1, encodedImage);
    }

}

int main (int argc, char **argv) {

    char* inputFile = "";
    char* outputFile = "";
    char* secretMessage = "";

    char c;
    while ((c = getopt(argc, argv, "i:o:m:")) != -1)
        switch (c)
        {
            case 'i':
                inputFile = optarg;
                break;
            case 'o':
                outputFile = optarg;
                break;
            case 'm':
                secretMessage = optarg;
                break;
            default:
                fprintf(stderr, "Please enter all necessary arguments.");
                exit(1);
        }


    FILE* originalImage = fopen(inputFile, "rb");
    FILE* encodedImage = fopen(outputFile, "wb");

    // Find the size of the file
    int fileSize = 0;
    fseek(originalImage, 2, SEEK_SET);
    fread(&fileSize, 4, 1, originalImage);

    int pixelArrayOffset = logInfo(originalImage);
    encodeImage(originalImage, encodedImage, secretMessage, fileSize, pixelArrayOffset);

    fclose(originalImage);
    fclose(encodedImage);

    return 0;
}


