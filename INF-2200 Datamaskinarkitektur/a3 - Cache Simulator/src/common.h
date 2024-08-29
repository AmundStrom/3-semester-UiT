/** @file common.h
 *  @brief Header files that define and declare the different structs used by the cache, 
 *  and define the functions used by the struct.
 *  @see memory.c
 */

#define fully 0
#define direct 1
#define twoway 2
#define fourway 4
#define eightway 8

#ifndef COMMON_H
#define COMMON_H

/**
 * @brief Struct to hold parameters for the caches.
 * @struct parameter
 * @param associative The associative of the cache; 0 -> Fully, 1 -> Direct, 2 -> 2-way, 4 -> 4-way, 8 -> 8-way
 * @param num_blocks Number of blocks in each set
 * @param num_sets Number of sets in cache
 */
typedef struct parameter parameter_t;


/**
 * @brief Struct to hold a general cache.
 * @struct cache
 */
typedef struct cache cache_t;


/**
 * @brief struct to hold a block of memory.
 * @struct block
 */
typedef struct block block_t;


/**
 * @brief Defines the replacment policy function type.
 * @param index The index/set to be accessed
 * @param action The action to preform on the cache and the block in the index/set to be accessed if necessary.
 * @param tag The tag to be placed in the cache
 * @param address The address, l2 has different parameters, so we split address again
 */
typedef void (*rep_policy_t)(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int action);


/**
 * @brief Defines the replacment policy function type.
 * @param index The index/set to be accessed
 * @param tag The tag to be placed in the cache
 * @param ret The return array, contains the action to preform on the cache and the block in the index/set to be accessed if necessary.
 */
typedef void (*write_policy_t)(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int ret[]);


struct parameter
{
    /* Cache spesific variables */
	int cache_size;
	int block_size;
	int bus_width;
	int associative;
     
    int num_blocks;
    int num_sets;

    /* Variables about address */
    int set_bits;
    int offset_bits;
    int tag_bits;
    
    /* Pointer functions to variable policies */
    rep_policy_t rep_policy;
    write_policy_t write_policy;
};


struct block
{
	int valid;
    int dirty;
	int tag;
    int counter;
};


struct cache
{
    parameter_t *para;
    block_t ***set;
    int hit;
    int miss;
};


/**
 * @brief Creates the parameters used for the cache.
 * @param cache_size Total cache size in KB
 * @param block_size Size of each individuell block in Bytes
 * @param associative The associative for the cache; 0 -> Fully, 1 -> Direct, 2 -> 2-way, 4 -> 4-way, 8 -> 8-way
 * @param replace The replacment policy for the cache
 * @param write The write policy for the cache
 * @returns pointer to parameter struct
 */
parameter_t *parameter_create(int cache_size, int block_size, int associative, rep_policy_t replace, write_policy_t write);


/**
 * @brief Destroy the parameter_t struct.
 */
void parameter_destory(parameter_t *para);


/**
 * @brief Creates new empty cache with the given parameters.
 * @param para stores a parameter struct inside it
 * @returns pointer to cache
 */
cache_t *cache_create(parameter_t *para);


/**
 * @brief Destroy the cache_t struct.
 */
void cache_destroy(cache_t *cache);


/**
 * @brief Creates new empty block.
 * @returns pointer to block
 */
block_t *block_create();


/**
 * @brief Destroy the block_t struct.
 */
void block_destroy(block_t *block);


/**
 * @brief A general associative policy function.
 * @return -2 = replace a tag on x block (MISS), -1 = do nothing (MISS), x >= 0 -> hit on x block (HIT)
 * @param index The index/set to be accessed
 * @param tag The tag to be placed in the cache
 */
int associative(cache_t *cache, int index, int tag);


/**
 * @brief Write through policy function.
 * @returns ARRAY | returns array of 2 elements corresponding to l1 and l2 cache, -2 = replace, -1 = do nothing, x >= 0 = hit on x block 
 * @param index The index/set to be accessed
 * @param tag The tag to be placed in the cache
 * @param ret The return array, contains action of each cache
 */
void write_through(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int ret[]); 


/**
 * @brief Write through policy function.
 * @returns ARRAY | returns array of 2 elements corresponding to l1 and l2 cache, -2 = replace, -1 = do nothing, x >= 0 = hit on x block 
 * @param index The index/set to be accessed
 * @param tag The tag to be placed in the cache
 * @param ret The return array, contains action of each cache
 */
void write_back(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int ret[]); 


/**
 * @brief Least Recently Used replacment policy. The block with the heighest counter is Least Recently Used. Handles dirty data aswell
 * @param index The index/set to be accessed
 * @param action The action to prefrom on the cache, and the block to get its counter reset.
 * @param tag The tag to be placed in the cache
 * @param address The address, l2 has different parameters, so we split address again
 * @returns nothing
 */
void lru(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int action);


/**
 * @brief Least Frequently Used replacment policy. The block with the lowest counter is Least Frequently Used. Handles dirty data aswell
 * @param index The index/set to be accessed
 * @param action The action to prefrom on the cache, and the block to get its counter reset.
 * @param tag The tag to be placed in the cache
 * @param address The address, l2 has different parameters, so we split address again
 * @returns nothing
 */
void lfu(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int action);


/**
 * @brief First In First Out replacment policy. The block with the heighest counter is the first element. Handles dirty data aswell
 * @param index The index/set to be accessed
 * @param action The action to prefrom on the cache
 * @param tag The tag to be placed in the cache
 * @param address The address, l2 has different parameters, so we split address again
 * @returns nothing
 */
void fifo(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int action);


/**
 * @brief First In First Out replacment policy. The block with the heighest counter is the first element. Handles dirty data aswell
 * @param index The index/set to be accessed
 * @param action The action to prefrom on the cache
 * @param tag The tag to be placed in the cache
 * @param address The address, l2 has different parameters, so we split address again
 * @returns nothing
 */
void rnd(cache_t *l1, cache_t *l2, int l1_index, int l2_index, int l1_tag, int l2_tag, int action);


/**
 * @brief Helper function to print cache.
 */
void cache_print(cache_t *cache);


#endif