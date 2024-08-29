/** @file common.c
 *  @brief Implements functions used by the cache.
 *  @see common.h
 */

#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <math.h>
#include "common.h"


parameter_t *parameter_create(int cache_size, int block_size, int associative,  rep_policy_t replace, write_policy_t write)
{
	parameter_t *para = (parameter_t *)malloc(sizeof(parameter_t));
	para->cache_size = cache_size;
	para->block_size = block_size;
    para->associative = associative;
	para->rep_policy = replace;
    para->write_policy = write;

    int total_blocks = (para->cache_size * 1024) / (para->block_size * 8);
    
	if (associative == 0)
		para->num_sets = 1;
	else
		para->num_sets = total_blocks / associative;

	para->num_blocks = total_blocks / para->num_sets;

    para->set_bits = log2(para->num_sets);
    para->offset_bits = log2(para->block_size);
    para->tag_bits = 32 - para->set_bits - para->offset_bits;

	return para;
}


void parameter_destory(parameter_t *para)
{
    free(para);
}


cache_t *cache_create(parameter_t *para)
{
	cache_t *cache = (cache_t *)malloc(sizeof(cache_t));
    cache->para = para;
    cache->hit = 0;
    cache->miss = 0;

	/* Allocating enough space to store 'x' number of sets. */
    cache->set = (block_t***)malloc(cache->para->num_sets * sizeof(block_t));
    for (int i = 0; i < cache->para->num_sets; i++){
        cache->set[i] = (block_t**)malloc(cache->para->num_blocks * sizeof(block_t));
    }

	/* Fill the cache with blocks in every set */
	for (int i = 0; i < cache->para->num_sets; i++){
		for (int j = 0; j < cache->para->num_blocks; j++){
            block_t *block = block_create();
            cache->set[i][j] = block;
		}
    }

	return cache;
}


void cache_destroy(cache_t *cache)
{
    for(int i = 0; i < cache->para->num_sets; i++)
    {
        for(int j = 0; j < cache->para->num_blocks; j++)
        {
            block_destroy(cache->set[i][j]);
        }
        free(cache->set[i]);
    }
    free(cache->set);

    parameter_destory(cache->para);

    free(cache);
}


block_t *block_create()
{
	block_t *block = malloc(sizeof(block_t));

	block->valid = 0;
    block->tag = 0;
    block->counter = 0;
    block->dirty = 0;
    return block;
}


void block_destroy(block_t *block)
{
    free(block);
}

int associative(cache_t *cache, int index, int tag)
{
    for(int i = 0; i < cache->para->num_blocks; i++){
        /* Found invalid block */
		if(cache->set[index][i]->valid == 0){
			cache->set[index][i]->tag = tag;
			cache->set[index][i]->valid = 1;
            cache->set[index][i]->dirty = 0;
			cache->miss++;
			return -1;
		}
        /* Found matching tag */
		if(cache->set[index][i]->tag == tag){
            cache->hit++;
			return i;
		}
	}
    /* No invalid block or matching tag, must replace */
    cache->miss++;
    return -2;
}


void write_through(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int ret[]) {

    /* Search in L1 */
   for(int i = 0; i < l1->para->num_blocks; i++){
        /* Found invalid block */
		if(l1->set[l1_index][i]->valid == 0){
			l1->set[l1_index][i]->tag = l1_tag;
			l1->set[l1_index][i]->valid = 1;
            l1->set[l1_index][i]->dirty = 0;
			l1->miss++;
			ret[0] = -1;
            break;
		}
        /* Found matching tag */
		if(l1->set[l1_index][i]->tag == l1_tag){
            l1->hit++;
            ret[0] = i;
			break;
		}
        /* No invalid block or matching tag, must replace */
        if( i == (l1->para->num_blocks - 1) ){
            l1->miss++;
            ret[0] = -2;
            break;
        }
	}

    /* Search in L2 */
    for(int i = 0; i < l2->para->num_blocks; i++){
        /* Found invalid block */
		if(l2->set[l2_index][i]->valid == 0){
			l2->set[l2_index][i]->tag = l2_tag;
			l2->set[l2_index][i]->valid = 1;
            l2->set[l2_index][i]->dirty = 0;
			l2->miss++;
			ret[1] = -1;
            break;
		}
        /* Found matching tag */
		if(l2->set[l2_index][i]->tag == l2_tag){
            l2->hit++;
            ret[1] = i;
			break;
		}
        /* No invalid block or matching tag, must replace */
        if( i == (l2->para->num_blocks - 1) ){
            l2->miss++;
            ret[1] = -2;
            break;
        }
	}
}

void write_back(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int ret[]) {

    for (int i = 0; i < l1->para->num_blocks; i++) {
        /* Found invalid block */
        if (l1->set[l1_index][i]->valid == 0) {
            l1->set[l1_index][i]->tag = l1_tag;
            l1->set[l1_index][i]->valid = 1;
            l1->set[l1_index][i]->dirty = 1;
            l1->miss++;
            
            ret[0] = -1;
            ret[1] = -1;
            return;
        }
        /* Found matching tag */
        if (l1->set[l1_index][i]->tag == l1_tag) {
            l1->set[l1_index][i]->dirty = 1;
            l1->hit++;

            /* Write back does not write to l2, we mark dirty*/
            ret[0] = i;
            ret[1] = -1;
            return;
        }
    }
    /* Exited loop without finding any tag or invalid block, need to replace all*/
    l1->miss++;
    ret[0] = -2;
    ret[1] = -1;
    return;
}


void lru(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int action)
{
    /* Increment counter for evey block that is valid */
    for(int i = 0; i < l1->para->num_blocks; i++)
        if(l1->set[l1_index][i]->valid == 1)
            l1->set[l1_index][i]->counter++;

    /* Hit! Reset counter on block */
    if(action >= 0)
        l1->set[l1_index][action]->counter = 0;
    /* Miss! Replace block with greatest counter */
    if(action == -2){
        int lru = 0, replace = 0;
        for(int i = 0; i < l1->para->num_blocks; i++)
            if(lru < l1->set[l1_index][i]->counter){
                lru = l1->set[l1_index][i]->counter;
                replace = i;
            }
        /* Check for dirty tag, pass to l2 */
        if (l1->set[l1_index][replace]->dirty == 1) {
            if (l2 != NULL) {
                int ret = associative(l2, l2_index, l2_tag);
                l2->para->rep_policy(l2, NULL, l2_index, 0, l2_tag, 0, ret);
            }
        }
        l1->set[l1_index][replace]->counter = 0;
        l1->set[l1_index][replace]->tag = l1_tag;
    }
}


void lfu(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int action)
{
    /* Increment counter for evey block that is valid */
    for(int i = 0; i < l1->para->num_blocks; i++)
        if(l1->set[l1_index][i]->valid == 1)
            l1->set[l1_index][i]->counter++;

    /* Hit! Reset counter on block */
    if(action >= 0)
        l1->set[l1_index][action]->counter = 0;
    /* Miss! Replace block with lowest counter */
    if(action == -2){
        int lfu = l1->set[l1_index][0]->counter, replace = 0;
        for(int i = 0; i < l1->para->num_blocks; i++)
            if(lfu > l1->set[l1_index][i]->counter){
                lfu = l1->set[l1_index][i]->counter;
                replace = i;
            }
        /* Check for dirty tag, pass to l2 */
        if (l1->set[l1_index][replace]->dirty == 1) {
            if (l2 != NULL) {
                int ret = associative(l2, l2_index, l2_tag);
                l2->para->rep_policy(l2, NULL, l2_index, 0, l2_tag, 0, ret);
            }
        }
        l1->set[l1_index][replace]->counter = 0;
        l1->set[l1_index][replace]->tag = l1_tag;
    }
}


void fifo(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int action)
{
    /* Increment counter for evey block that is valid */
    for(int i = 0; i < l1->para->num_blocks; i++)
        if(l1->set[l1_index][i]->valid == 1)
            l1->set[l1_index][i]->counter++;

    /* Miss! Replace block with greatest counter */
    if(action == -2){
        int lru = 0, replace = 0;
        for(int i = 0; i < l1->para->num_blocks; i++)
            if(lru < l1->set[l1_index][i]->counter){
                lru = l1->set[l1_index][i]->counter;
                replace = i;
            }
        /* Check for dirty tag, pass to l2 */
        if (l1->set[l1_index][replace]->dirty == 1) {
            if (l2 != NULL) {
                int ret = associative(l2, l2_index, l2_tag);
                l2->para->rep_policy(l2, NULL, l2_index, 0, l2_tag, 0, ret);
            }
        }
        l1->set[l1_index][replace]->counter = 0;
        l1->set[l1_index][replace]->tag = l1_tag;
    }
}


void rnd(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int action)
{
    /* Miss! Replace a random block */
    if(action < 0){
        int replace = rand() % l1->para->num_blocks;
        /* Check for dirty tag, pass to l2 */
        if (l1->set[l1_index][replace]->dirty == 1) {
            if (l2 != NULL) {
                int ret = associative(l2, l2_index, l2_tag);
                l2->para->rep_policy(l2, NULL, l2_index, 0, l2_tag, 0, ret);
            }
        }
        l1->set[l1_index][replace]->tag = l1_tag;
    }
}


void cache_print(cache_t *cache){
    for(int i = 0; i < cache->para->num_sets; i++){
        printf("======= Set: %i =======\n", i);
        for(int j = 0; j < cache->para->num_blocks; j++){
            printf("--- Block %i; tag: %i, valid: %i, counter: %i\n",
                    j, cache->set[i][j]->tag, cache->set[i][j]->valid, cache->set[i][j]->counter);
        }
        printf("======= Set: %i =======\n\n", i);
    }
}