/** @file cpu.c
 *  @brief This code simulates a system with caching between the CPU and the
 *  main memory.
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include "memory.h"
#include "byutr.h"
#include "common.h"

/*
* Command line argument: Trace file.
*/
int main(int argc, char *argv[])
{
    srand(time(NULL));
	FILE *tracef;
	p2AddrTr tr;

	if (argc < 2)
	{
		printf("Usage: %s filename\n", argv[0]);
		exit(1);
	}

	/* fopen(argv[1], "r") -> fopen(argv[1], "rb")
	* Windows doesn't follow POSIX here and fopen needs the 'b' to function
	* properly.
	*/
	if ((tracef = fopen(argv[1], "rb")) == NULL)
	{
		printf("Could not open file: %s\n", argv[1]);
		exit(1);
	}

    /* Total cache size in KB */
	int l1_cache_size = 32;
    int l2_cache_size = 256;

    /* Size of each individuell block in Bytes */
    int block_size = 64;

    /*  The associativity of the cache;
     *  0 -> Fully Associative
     *  1 -> Direct Mapping
     *  2 -> 2-way set-Associative
     *  4 -> 4-way set-Associative
     *  8 -> 8-way set-Associative
     */
    int l1instr_assoc = fourway;
	int l1data_assoc = eightway;
    int l2unif_assoc = eightway;

    /*  The replacment policy for the cache 
     *  lru -> Least Recently Used
     *  lfu -> Least Frequently Used 
     *  fifo -> First In First Out
     *  rnd -> Random
     */
    void *rep_policy = rnd;
	void *write_poicy = write_back;

	/*  The write policy for the cache 
     *  write_through
	 *	write_back
     */
	void *write_policy = write_back;

    /* Initialize the parameters for the caches */
	parameter_t *l1Ins_para = parameter_create(l1_cache_size, block_size, l1instr_assoc, rep_policy, write_policy);
    parameter_t *l1Data_para = parameter_create(l1_cache_size, block_size, l1data_assoc, rep_policy, write_policy);
    parameter_t *l2Uni_para = parameter_create(l2_cache_size, block_size, l2unif_assoc, rep_policy, write_policy);

    /* Initialize the different cahces with the given parameters */
    cache_t *l1Ins = cache_create(l1Ins_para);
    cache_t *l1Data = cache_create(l1Data_para);
    cache_t *l2Uni = cache_create(l2Uni_para);

	memory_init(); /* Initialize the memory subsystem */

	/* Loop through the trace file and simulate memory accesses */
	while (!feof(tracef))
	{
		if (fread(&tr, sizeof(p2AddrTr), 1, tracef) == 1)
		{
			switch(tr.reqtype)
			{
				case FETCH:    memory_fetch(tr.addr, NULL, l1Ins, l2Uni); break;
				case MEMREAD:  memory_read(tr.addr, NULL, l1Data, l2Uni); break;
				case MEMWRITE: memory_write(tr.addr, NULL, l1Data, l2Uni); break;
				default: printf("Ignoring trace record with type %d\n", tr.reqtype);
			}		
		}
	}

    printf("Instruction cache hit: %i and miss: %i\n",l1Ins->hit, l1Ins->miss);
    printf("Data cache hit: %i and miss: %i\n",l1Data->hit, l1Data->miss);
    printf("Unified cache hit: %i and miss: %i\n",l2Uni->hit, l2Uni->miss);
	// cache_print(l1Ins);
	// cache_print(l1Data);
	// cache_print(l2Uni);

	fclose(tracef);

	/* Deinitialize the caches */
	cache_destroy(l1Ins);
	cache_destroy(l1Data);
	cache_destroy(l2Uni);
	memory_finish(); /* Deinitialize the memory subsystem */

	return 0;
}
