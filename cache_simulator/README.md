This C program simulates the behavior of a cache memory. The program takes a valgrind memory trace as input,
simulates the hit/miss behavior of a cache memory on this trace, and outputs the total number of hits,
misses, and evictions. It uses the LRU replacement policy when choosing a cache line to evict.

The reference simulator takes the following command-line arguments:
  Usage: ./csim-ref [-v] -s <s> -E <E> -b <b> -t <tracefile>
    • -v: Optional verbose flag that displays trace info
    • -s <s>: Number of set index bits
    • -E <E>: Associativity (number of lines per set)
    • -b <b>: Number of block bits
    • -t <tracefile>: Name of the valgrind trace to replay
  
