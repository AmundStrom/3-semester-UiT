/** @file memory.c
 *  @brief Implements starting point for a memory hierarchy with caching and RAM.
 *  @see memory.h
 */

#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include "memory.h"
#include "common.h"

static unsigned long instr_count = 0;

int get_tag(parameter_t *para, unsigned int address) {
	return abs(address >> (32 - para->tag_bits));
}

int get_index(parameter_t *para, unsigned int address) {

	int index = 0;
	if (para->associative > 0) {
		index = address << (para->tag_bits);
		index = index >> (para->tag_bits + para->offset_bits);
	}

	return abs(index);
}

void memory_init(void)
{
	/* Initialize memory subsystem here. */
	
	instr_count = 0;
}

void memory_fetch(unsigned int address, data_t *data, cache_t *l1, cache_t *l2)
{
	// printf("memory: fetch decimal %d\n", address);
	if (data)
		*data = (data_t) 0;

	/* We use shifting to produce the relevant bits of information we need, tag and index */
	int l1_tag = get_tag(l1->para, address);
	int l2_tag = get_tag(l2->para, address);

	/* Index bit defaults to 0 in case of fully associative cache */
	int l1_index = get_index(l1->para, address);
	int l2_index = get_index(l2->para, address);

	/* Search in L1 */
	int ret = associative(l1, l1_index, l1_tag);
	l1->para->rep_policy(l1, l2, l1_index, l2_index, l1_tag, l2_tag, ret);

	/* If L1 miss, search in L2 */
	if (ret < 0)
	{
		ret = associative(l2, l2_index, l2_tag);
		l2->para->rep_policy(l2, NULL, l2_index, 0, l2_tag, 0, ret);
	}

	instr_count++;
	// printf("INST--- Count: %ld, l1->hit %i, l1->miss %i, l2->hit %i, l2->miss %i\n", 
	// 	    instr_count, l1->hit, l1->miss, l2->hit, l2->miss);
}

void memory_read(unsigned int address, data_t *data, cache_t *l1, cache_t *l2)
{
	// printf("memory: read decimal %d\n", address);
	if (data)
		*data = (data_t) 0;
	
	/* We use shifting to produce the relevant bits of information we need, tag and index */
	int l1_tag = get_tag(l1->para, address);
	int l2_tag = get_tag(l2->para, address);

	/* Index bit defaults to 0 in case of fully associative cache */
	int l1_index = get_index(l1->para, address);
	int l2_index = get_index(l2->para, address);

	/* Search in L1 */
	int ret = associative(l1, l1_index, l1_tag);
	l1->para->rep_policy(l1, l2, l1_index, l2_index, l1_tag, l2_tag, ret);

	// printf("hit?\n");
	/* If L1 miss, search in L2 */
	if (ret < 0)
	{
		ret = associative(l2, l2_index, l2_tag);
		l2->para->rep_policy(l2, NULL, l2_index, 0, l2_tag, 0, ret);
	}

	instr_count++;
	// printf("DATA--- Count: %ld, l1->hit %i, l1->miss %i, l2->hit %i, l2->miss %i\n", 
	// 	    instr_count, l1->hit, l1->miss, l2->hit, l2->miss);
}

void memory_write(unsigned int address, data_t *data, cache_t *l1, cache_t *l2)
{
	// printf("memory: write decimal %d\n", address);
	if (data)
		*data = (data_t) 0;

	int ret[2];

	/* We use shifting to produce the relevant bits of information we need, tag and index */
	int l1_tag = get_tag(l1->para, address);
	int l2_tag = get_tag(l2->para, address);

	/* Index bit defaults to 0 in case of fully associative cache */
	int l1_index = get_index(l1->para, address);
	int l2_index = get_index(l2->para, address);

	/* Writes 'new' data to cache. If it misses and no space, we utilize replacement policy */
	l1->para->write_policy(l1, l2, l1_index, l2_index, l1_tag, l2_tag, ret);

	/* Replace on l1 and l2 */
	l1->para->rep_policy(l1, l2, l1_index, l2_index, l1_tag, l2_tag, ret[0]);
	l2->para->rep_policy(l2, NULL, l2_index, 0, l2_tag, 0, ret[1]);

	instr_count++;
	// printf("DATA--- Count: %ld, l1->hit %i, l1->miss %i, l2->hit %i, l2->miss %i\n", 
	// 	    instr_count, l1->hit, l1->miss, l2->hit, l2->miss);
}

void memory_finish(void)
{
	fprintf(stdout, "Executed %lu instructions.\n\n", instr_count);
	
	/* Deinitialize memory subsystem here */
}
