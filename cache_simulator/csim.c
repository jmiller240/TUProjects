#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <getopt.h>
#include "cachelab.h"
#include <string.h>

int hit_count, miss_count, eviction_count;

typedef unsigned long mem_addr_t;
typedef unsigned long lru_t;

/* One cache line */
typedef struct
{
    char valid;     ///* Non-zero means line is valid */
    mem_addr_t tag; /* Tag bits from address */
    lru_t lru;      /* Least-recently-used value */
} cache_line_t;

/* One cache set: an array of E cache lines */
typedef cache_line_t *cache_set_t;

/* One cache: an array of S cache sets */
typedef cache_set_t *cache_t;

char *trace_file_name; /* Name of the trace file */
int E = 1;             /* Number of lines per set */
int s = 1;
int b = 1;
int v = 0;

// Address essentials
unsigned long addrTag = 0;
unsigned long setIndex = 0;
unsigned long timeStamp = 1;

// Go cachein
char *loadOrStore(cache_t cache, unsigned long addrTag, unsigned long set)
{

    char *result = "A";
    cache_line_t evict; // The line to evict, if needed
    evict.lru = timeStamp;
    int line;

    for (line = 0; line < E; line++)
    {
        if ((cache[set][line].tag == addrTag) && (cache[set][line].valid == '1'))
        {
            result = "hit";
            hit_count++;
            cache[set][line].lru = timeStamp;
            timeStamp++;
            return result;
        }

        // Evict the line if invalid or if it is less recently used than the current LRU
        if (cache[set][line].valid == '0')
        {
            evict.lru = cache[set][line].lru;
        }
        else if (cache[set][line].lru <= evict.lru)
        {
            evict.lru = cache[set][line].lru;
        }
    }

    // If no hit, set miss and check for evictionS
    result = "miss";
    miss_count++;
    for (line = 0; line < E; line++)
    {
        if (cache[set][line].lru == evict.lru)
        {
            if (cache[set][line].valid == '1')
            {
                result = "miss eviction";
                eviction_count++;
                cache[set][line].tag = addrTag;
                cache[set][line].lru = timeStamp;
                timeStamp++;
            }
            else
            {
                cache[set][line].valid = '1';
                cache[set][line].tag = addrTag;
                cache[set][line].lru = timeStamp;
                timeStamp++;
            }
            return result;
        }
    }
    return result;
}

int main(int argc, char **argv)
{
    char c;

    /* A start on processing command-line arguments. See `man 3 getopt` for details. */
    while ((c = getopt(argc, argv, "vs:E:b:t:h")) != -1)
    {
        switch (c)
        {
        case 'v':
            v = 1;
            break;
        case 's': /* Set number of sets per cache */
            s = atoi(optarg);
            break;
        case 'E': /* Set number of lines per set. */
            E = atoi(optarg);
            break;
        case 'b':
            b = atoi(optarg);
            break;
        case 't': /* Set name of file to read. */
            trace_file_name = optarg;
            break;
        default: /* Offer assistance. */
        case 'h':
            fprintf(stderr, "usage: ...\n");
            exit(1);
        }
    }

    printf("v=%d; s=%d; E=%d; b=%d; t=%s\n", v, s, E, b, trace_file_name);

    hit_count = 0;
    miss_count = 0;
    eviction_count = 0;

    /* Initialize cache */
    cache_t one_cache = (cache_t)malloc((1 << s) * sizeof(cache_set_t));

    int r, l;
    for (r = 0; r < (1 << s); r++)
    {
        one_cache[r] = (cache_set_t)malloc(E * sizeof(cache_line_t));
        for (l = 0; l < E; l++)
        {
            one_cache[r][l].valid = '0';
        }
    }

    /* How to read from the trace file. */
    char operation;     /* The operation (I, L, S, M) */
    mem_addr_t address; /* The address (in hex) */
    int size;
    char *result;

    FILE *tfp = fopen(trace_file_name, "r");
    while (fscanf(tfp, " %c %lx,%x\n", &operation, &address, &size) != EOF)
    {

        // Set address parameters
        addrTag = address >> (s + b);
        setIndex = (address >> b) & (~(~0 << s));

        // Go cachin
        if (operation == 'I')
        {
            continue;
        }
        else if ((operation == 'L') || (operation == 'S'))
        {
            result = loadOrStore(one_cache, addrTag, setIndex);
        }
        else // If M, the load is always followed by a store, which always hits
        {
            result = loadOrStore(one_cache, addrTag, setIndex);
            hit_count++;
        }

        if (v)
        {
            printf("%c %lx,%x    %s\n", operation, address, size, result);
        }
        else
        {
            printf("%c %lx,%x\n", operation, address, size);
        }
    }
    fclose(tfp);

    // Return memory to manager
    for (r = 0; r < (1 << s); r++)
    {
        free(one_cache[r]);
    }

    free(one_cache);

    printSummary(hit_count, miss_count, eviction_count);

    return 0;
}
